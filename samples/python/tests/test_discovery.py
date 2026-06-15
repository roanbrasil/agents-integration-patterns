import pytest
from unittest.mock import MagicMock, patch


def mock_response(text: str) -> MagicMock:
    r = MagicMock()
    r.content = text
    return r


# ── agent_card_registry ────────────────────────────────────
def test_discover_agent_found():
    from discovery.agent_card_registry import discover_agent
    card = discover_agent("translation")
    assert card is not None
    assert card["name"] == "translator_agent"


def test_discover_agent_not_found():
    from discovery.agent_card_registry import discover_agent
    assert discover_agent("unknown_capability_xyz") is None


def test_delegate_task_calls_llm():
    with patch("discovery.agent_card_registry.ChatAnthropic") as MockLLM:
        instance = MockLLM.return_value
        instance.invoke.return_value = mock_response("Olá, como vai você?")
        from discovery.agent_card_registry import delegate_task, REGISTRY
        card = REGISTRY["translator_agent"]
        result = delegate_task(card, "Translate: Hello, how are you?")
        assert result == "Olá, como vai você?"


# ── agent_proxy ────────────────────────────────────────────
def test_agent_proxy_success():
    from discovery.agent_proxy import agent_proxy
    dummy_agent = MagicMock(return_value="done")
    result = agent_proxy("task", dummy_agent, max_retries=1)
    assert result == "done"
    dummy_agent.assert_called_once_with("task")


def test_agent_proxy_retries_then_succeeds():
    from discovery.agent_proxy import agent_proxy
    call_count = {"n": 0}
    def flaky(t):
        call_count["n"] += 1
        if call_count["n"] < 2:
            raise RuntimeError("transient")
        return "recovered"
    result = agent_proxy("task", flaky, max_retries=2)
    assert result == "recovered"
    assert call_count["n"] == 2


def test_agent_proxy_raises_after_max_retries():
    from discovery.agent_proxy import agent_proxy
    def always_fails(t):
        raise RuntimeError("always fails")
    with pytest.raises(RuntimeError, match="All"):
        agent_proxy("task", always_fails, max_retries=1)
