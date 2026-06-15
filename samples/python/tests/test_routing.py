from unittest.mock import MagicMock, patch


def mock_response(text: str) -> MagicMock:
    r = MagicMock()
    r.content = text
    return r


# ── content_based_router ───────────────────────────────────
def test_router_agent_returns_coding():
    with patch("routing.content_based_router.llm") as m:
        m.invoke.return_value = mock_response("coding")
        from routing.content_based_router import router_agent
        assert router_agent("How to reverse a list?") == "coding"


def test_router_agent_returns_research():
    with patch("routing.content_based_router.llm") as m:
        m.invoke.return_value = mock_response("research")
        from routing.content_based_router import router_agent
        assert router_agent("What caused WWI?") == "research"


def test_router_agent_defaults_to_research_on_unknown():
    with patch("routing.content_based_router.llm") as m:
        m.invoke.return_value = mock_response("unknown_garbage")
        from routing.content_based_router import router_agent
        assert router_agent("something weird?") == "research"


# ── scatter_gather ─────────────────────────────────────────
def test_scatter_returns_one_per_role():
    with patch("routing.scatter_gather.llm") as m:
        m.invoke.return_value = mock_response("interesting perspective")
        from routing.scatter_gather import scatter, AGENT_ROLES
        results = scatter("Should AI be regulated?")
        assert len(results) == len(AGENT_ROLES)
        assert all(r == "interesting perspective" for r in results)


def test_gather_returns_synthesis():
    with patch("routing.scatter_gather.llm") as m:
        m.invoke.return_value = mock_response("Balanced synthesis.")
        from routing.scatter_gather import gather
        result = gather("question", ["p1", "p2", "p3"])
        assert result == "Balanced synthesis."


# ── pipeline ──────────────────────────────────────────────
def test_pipeline_planner_node():
    with patch("routing.pipeline.llm") as m:
        m.invoke.return_value = mock_response("Step 1: define. Step 2: do.")
        from routing.pipeline import planner
        result = planner({"task": "write tests", "plan": "", "result": "", "verified": ""})
        assert result["plan"] == "Step 1: define. Step 2: do."


def test_pipeline_executor_node():
    with patch("routing.pipeline.llm") as m:
        m.invoke.return_value = mock_response("Tests written.")
        from routing.pipeline import executor
        result = executor({"task": "write tests", "plan": "some plan", "result": "", "verified": ""})
        assert result["result"] == "Tests written."


def test_pipeline_verifier_node():
    with patch("routing.pipeline.llm") as m:
        m.invoke.return_value = mock_response("PASS — result addresses the task.")
        from routing.pipeline import verifier
        result = verifier({"task": "write tests", "plan": "plan", "result": "Tests written.", "verified": ""})
        assert "PASS" in result["verified"]
