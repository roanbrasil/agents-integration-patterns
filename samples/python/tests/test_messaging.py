import pytest
from unittest.mock import MagicMock, patch


# ── helpers ────────────────────────────────────────────────
def mock_response(text: str) -> MagicMock:
    r = MagicMock()
    r.content = text
    return r


# ── direct_message ─────────────────────────────────────────
def test_direct_message_agent_a():
    with patch("messaging.direct_message.llm") as m:
        m.invoke.return_value = mock_response("What is the farthest planet?")
        from messaging.direct_message import agent_a
        result = agent_a({"question": "", "answer": ""})
        assert result["question"] == "What is the farthest planet?"
        assert result["answer"] == ""


def test_direct_message_agent_b():
    with patch("messaging.direct_message.llm") as m:
        m.invoke.return_value = mock_response("Neptune is the farthest planet.")
        from messaging.direct_message import agent_b
        state = {"question": "What is the farthest planet?", "answer": ""}
        result = agent_b(state)
        assert result["answer"] == "Neptune is the farthest planet."


# ── broadcast_message ──────────────────────────────────────
def test_broadcast_publisher():
    with patch("messaging.broadcast_message.llm") as m:
        m.invoke.return_value = mock_response("AI cures all bugs!")
        from messaging.broadcast_message import publisher
        assert publisher() == "AI cures all bugs!"


def test_broadcast_subscriber():
    with patch("messaging.broadcast_message.llm") as m:
        m.invoke.return_value = mock_response("Fascinating! This changes everything.")
        from messaging.broadcast_message import subscriber
        result = subscriber("Optimist", "Be positive.", "AI cures bugs!")
        assert result == "Fascinating! This changes everything."


# ── blackboard ─────────────────────────────────────────────
def test_blackboard_agent_a():
    with patch("messaging.blackboard.llm") as m:
        m.invoke.return_value = mock_response("P vs NP remains unsolved.")
        from messaging.blackboard import agent_a
        board: dict = {}
        agent_a(board)
        assert board["problem"] == "P vs NP remains unsolved."


def test_blackboard_agent_b():
    with patch("messaging.blackboard.llm") as m:
        m.invoke.return_value = mock_response("Use approximation algorithms.")
        from messaging.blackboard import agent_b
        board = {"problem": "P vs NP"}
        agent_b(board)
        assert board["partial_solution"] == "Use approximation algorithms."
