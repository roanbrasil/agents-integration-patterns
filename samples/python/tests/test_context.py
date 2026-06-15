from unittest.mock import MagicMock, patch


def mock_response(text: str) -> MagicMock:
    r = MagicMock()
    r.content = text
    return r


# ── context_injection ──────────────────────────────────────
def test_fetch_resource_user_profile():
    from context.context_injection import fetch_resource
    profile = fetch_resource("user_profile")
    assert profile["name"] == "Alice"
    assert profile["role"] == "Data Scientist"


def test_build_context_prompt_contains_question():
    from context.context_injection import build_context_prompt
    prompt = build_context_prompt("What is LangGraph?")
    assert "What is LangGraph?" in prompt
    assert "Alice" in prompt


def test_context_injection_invoke():
    with patch("context.context_injection.llm") as m:
        m.invoke.return_value = mock_response("LangGraph builds stateful agents.")
        from context.context_injection import build_context_prompt
        prompt = build_context_prompt("What is LangGraph?")
        result = m.invoke(prompt)
        assert result.content == "LangGraph builds stateful agents."


# ── tool_provider ──────────────────────────────────────────
def test_tool_server_list_tools():
    from context.tool_provider import ToolServer
    server = ToolServer()
    tools = server.list_tools()
    names = [t["name"] for t in tools]
    assert "calculate" in names
    assert "get_weather" in names


def test_tool_server_calculate():
    from context.tool_provider import ToolServer
    server = ToolServer()
    result = server.call_tool("calculate", {"expression": "2 + 3 * 4"})
    assert "14" in result


def test_tool_server_get_weather():
    from context.tool_provider import ToolServer
    server = ToolServer()
    result = server.call_tool("get_weather", {"city": "Paris"})
    assert "Paris" in result or "Sunny" in result


def test_tool_server_unknown_tool():
    from context.tool_provider import ToolServer
    server = ToolServer()
    result = server.call_tool("hack", {"x": "1"})
    assert "Unknown" in result or "hack" in result
