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
