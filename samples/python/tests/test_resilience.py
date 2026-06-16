import time
import pytest
from unittest.mock import MagicMock, patch


def mock_response(text: str) -> MagicMock:
    r = MagicMock()
    r.content = text
    return r


# ── dead_letter_agent ──────────────────────────────────────
def test_dead_letter_agent_node_fails_first_attempt():
    from resilience.dead_letter_agent import agent_node
    state = {"task": "do it", "result": "", "error": "", "retries": 0, "status": ""}
    result = agent_node(state)
    assert result["status"] == "failed"
    assert result["retries"] == 1


def test_dead_letter_agent_node_succeeds_on_retry():
    with patch("resilience.dead_letter_agent.llm") as m:
        m.invoke.return_value = mock_response("task done")
        from resilience.dead_letter_agent import agent_node
        state = {"task": "do it", "result": "", "error": "", "retries": 1, "status": ""}
        result = agent_node(state)
        assert result["status"] == "done"
        assert result["result"] == "task done"


def test_dead_letter_node_sets_dead_letter_status():
    from resilience.dead_letter_agent import dead_letter_node
    state = {"task": "do it", "result": "", "error": "fail", "retries": 2, "status": "failed"}
    result = dead_letter_node(state)
    assert result["status"] == "dead_letter"
    assert "DEAD LETTER" in result["result"]


# ── circuit_breaker ────────────────────────────────────────
def test_circuit_breaker_starts_closed():
    from resilience.circuit_breaker import CircuitBreaker
    cb = CircuitBreaker()
    assert cb.state == "CLOSED"


def test_circuit_breaker_opens_after_threshold():
    from resilience.circuit_breaker import CircuitBreaker
    cb = CircuitBreaker(failure_threshold=2)
    for _ in range(2):
        try:
            cb.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        except RuntimeError:
            pass
    assert cb.state == "OPEN"


def test_circuit_breaker_blocks_when_open():
    from resilience.circuit_breaker import CircuitBreaker
    cb = CircuitBreaker(failure_threshold=1)
    try:
        cb.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
    except RuntimeError:
        pass
    with pytest.raises(RuntimeError, match="OPEN"):
        cb.call(lambda: "ok")


def test_circuit_breaker_success_resets_failures():
    from resilience.circuit_breaker import CircuitBreaker
    cb = CircuitBreaker(failure_threshold=3)
    result = cb.call(lambda: "success")
    assert result == "success"
    assert cb.failure_count == 0


# ── checkpoint_resume ──────────────────────────────────────
def test_step1_research():
    with patch("resilience.checkpoint_resume.llm") as m:
        m.invoke.return_value = mock_response("LangGraph is a graph framework.")
        from resilience.checkpoint_resume import step1_research
        result = step1_research({"topic": "LangGraph", "step1_output": "", "step2_output": "", "step3_output": ""})
        assert result["step1_output"] == "LangGraph is a graph framework."


def test_step2_analyze():
    with patch("resilience.checkpoint_resume.llm") as m:
        m.invoke.return_value = mock_response("Challenge 1, Challenge 2")
        from resilience.checkpoint_resume import step2_analyze
        result = step2_analyze({"topic": "LG", "step1_output": "LangGraph is...", "step2_output": "", "step3_output": ""})
        assert result["step2_output"] == "Challenge 1, Challenge 2"


# ── idempotent_agent ───────────────────────────────────────
def test_idempotent_same_args_returns_cached_result():
    from implementation.idempotent_agent import IdempotencyGuard
    calls = {"n": 0}
    guard = IdempotencyGuard()
    def action(x: str) -> str:
        calls["n"] += 1
        return f"result:{x}"
    r1 = guard.execute("action", action, "hello")
    r2 = guard.execute("action", action, "hello")
    assert r1 == r2 == "result:hello"
    assert calls["n"] == 1  # only ran once


def test_idempotent_different_args_run_separately():
    from implementation.idempotent_agent import IdempotencyGuard
    calls = {"n": 0}
    guard = IdempotencyGuard()
    def action(x: str) -> str:
        calls["n"] += 1
        return f"result:{x}"
    guard.execute("action", action, "a")
    guard.execute("action", action, "b")
    assert calls["n"] == 2


def test_idempotent_decorator():
    from implementation.idempotent_agent import IdempotencyGuard
    guard = IdempotencyGuard()
    calls = {"n": 0}
    @guard.protect
    def do_work(x: int) -> int:
        calls["n"] += 1
        return x * 2
    assert do_work(5) == 10
    assert do_work(5) == 10  # cached
    assert calls["n"] == 1


# ── exception_handler_chain ────────────────────────────────
def test_retry_handler_recovers_on_transient_error():
    from implementation.exception_handler_chain import (
        ExceptionHandlerChain, RetryHandler, RateLimitError,
    )
    calls = {"n": 0}
    def flaky():
        calls["n"] += 1
        if calls["n"] < 2:
            raise RateLimitError("rate limited")
        return "ok"
    chain = ExceptionHandlerChain().add(RetryHandler(on=RateLimitError, max_retries=3))
    result = chain.execute(flaky)
    assert result.success
    assert result.value == "ok"
    assert result.handler_used == "retry"


def test_fallback_handler_delegates_on_format_error():
    from implementation.exception_handler_chain import (
        ExceptionHandlerChain, FallbackHandler, OutputFormatError,
    )
    def bad_agent(): raise OutputFormatError("bad json")
    def good_fallback(): return "fallback result"
    chain = ExceptionHandlerChain().add(FallbackHandler(on=OutputFormatError, fallback=good_fallback))
    result = chain.execute(bad_agent)
    assert result.success
    assert result.value == "fallback result"
    assert result.handler_used == "fallback"


def test_escalate_handler_marks_as_failed():
    from implementation.exception_handler_chain import ExceptionHandlerChain, EscalateHandler
    notified = {"exc": None}
    def notify(e): notified["exc"] = e
    def bad_agent(): raise ValueError("bad")
    chain = ExceptionHandlerChain().add(EscalateHandler(on=Exception, notify=notify))
    result = chain.execute(bad_agent)
    assert not result.success
    assert result.handler_used == "escalated"
    assert notified["exc"] is not None
