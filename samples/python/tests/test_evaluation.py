from unittest.mock import MagicMock, patch


def mock_response(text: str) -> MagicMock:
    r = MagicMock()
    r.content = text
    return r


# ── llm_as_judge ───────────────────────────────────────────
def test_produce_node():
    with patch("evaluation.llm_as_judge.llm") as m:
        m.invoke.return_value = mock_response("Microservices decouple services.")
        from evaluation.llm_as_judge import produce
        state = {"task": "explain microservices", "output": "", "verdict": "", "reason": "", "retries": 0}
        result = produce(state)
        assert result["output"] == "Microservices decouple services."


def test_judge_node_approved():
    with patch("evaluation.llm_as_judge.llm") as m:
        m.invoke.return_value = mock_response("APPROVED - clear and concise")
        from evaluation.llm_as_judge import judge
        state = {"task": "explain microservices", "output": "good answer", "verdict": "", "reason": "", "retries": 0}
        result = judge(state)
        assert result["verdict"] == "APPROVED"


def test_judge_node_rejected():
    with patch("evaluation.llm_as_judge.llm") as m:
        m.invoke.return_value = mock_response("REJECTED - too vague")
        from evaluation.llm_as_judge import judge
        state = {"task": "explain microservices", "output": "bad answer", "verdict": "", "reason": "", "retries": 0}
        result = judge(state)
        assert result["verdict"] == "REJECTED"


def test_route_approved_ends():
    from evaluation.llm_as_judge import route
    from langgraph.graph import END
    state = {"task": "t", "output": "o", "verdict": "APPROVED", "reason": "ok", "retries": 0}
    assert route(state) == "__end__"


def test_route_rejected_with_retries_goes_to_produce():
    from evaluation.llm_as_judge import route
    state = {"task": "t", "output": "o", "verdict": "REJECTED", "reason": "bad", "retries": 0}
    assert route(state) == "produce"


def test_route_rejected_max_retries_dead_letter():
    from evaluation.llm_as_judge import route
    state = {"task": "t", "output": "o", "verdict": "REJECTED", "reason": "bad", "retries": 2}
    assert route(state) == "dead_letter"


# ── ensemble_judge ─────────────────────────────────────────
def test_run_judge_approved():
    with patch("evaluation.ensemble_judge.llm") as m:
        m.invoke.return_value = mock_response("APPROVED - factually correct")
        from evaluation.ensemble_judge import run_judge
        result = run_judge("correctness", "check facts", "explain ML", "ML is learning from data.")
        assert result["verdict"] == "APPROVED"
        assert result["lens"] == "correctness"


def test_run_judge_rejected():
    with patch("evaluation.ensemble_judge.llm") as m:
        m.invoke.return_value = mock_response("REJECTED - off topic")
        from evaluation.ensemble_judge import run_judge
        result = run_judge("relevance", "check relevance", "explain ML", "Python is great.")
        assert result["verdict"] == "REJECTED"


def test_ensemble_judge_majority_approved():
    with patch("evaluation.ensemble_judge.llm") as m:
        m.invoke.side_effect = [
            mock_response("APPROVED - correct"),
            mock_response("APPROVED - safe"),
            mock_response("REJECTED - off topic"),
        ]
        from evaluation.ensemble_judge import ensemble_judge
        result = ensemble_judge("explain ML", "ML learns from data.")
        assert result == "APPROVED"


def test_ensemble_judge_majority_rejected():
    with patch("evaluation.ensemble_judge.llm") as m:
        m.invoke.side_effect = [
            mock_response("REJECTED - incorrect"),
            mock_response("REJECTED - harmful"),
            mock_response("APPROVED - relevant"),
        ]
        from evaluation.ensemble_judge import ensemble_judge
        result = ensemble_judge("explain ML", "bad answer here.")
        assert result == "REJECTED"
