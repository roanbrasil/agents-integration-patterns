from unittest.mock import MagicMock, patch


def mock_response(text: str) -> MagicMock:
    r = MagicMock()
    r.content = text
    return r


# ── supervised_delegation ──────────────────────────────────
def test_supervisor_split_returns_two_subtasks():
    with patch("coordination.supervised_delegation.llm") as m:
        m.invoke.return_value = mock_response("Subtask A\nSubtask B")
        from coordination.supervised_delegation import supervisor_split
        state = {"task": "analyze data", "subtasks": [], "worker_a_result": "", "worker_b_result": "", "final_review": ""}
        result = supervisor_split(state)
        assert len(result["subtasks"]) == 2
        assert result["subtasks"][0] == "Subtask A"


def test_worker_a_uses_first_subtask():
    with patch("coordination.supervised_delegation.llm") as m:
        m.invoke.return_value = mock_response("Worker A done")
        from coordination.supervised_delegation import worker_a
        state = {"task": "t", "subtasks": ["Do A", "Do B"], "worker_a_result": "", "worker_b_result": "", "final_review": ""}
        result = worker_a(state)
        assert result["worker_a_result"] == "Worker A done"


# ── orchestrator ───────────────────────────────────────────
def test_step1_gather():
    with patch("coordination.orchestrator.llm") as m:
        m.invoke.return_value = mock_response("Fact 1, Fact 2, Fact 3")
        from coordination.orchestrator import step1_gather
        result = step1_gather({"topic": "Kubernetes", "info": "", "analysis": "", "summary": ""})
        assert result["info"] == "Fact 1, Fact 2, Fact 3"


def test_step2_analyze():
    with patch("coordination.orchestrator.llm") as m:
        m.invoke.return_value = mock_response("Key insight: scalability")
        from coordination.orchestrator import step2_analyze
        result = step2_analyze({"topic": "K8s", "info": "facts", "analysis": "", "summary": ""})
        assert result["analysis"] == "Key insight: scalability"


def test_step3_summarize():
    with patch("coordination.orchestrator.llm") as m:
        m.invoke.return_value = mock_response("K8s simplifies deployment.")
        from coordination.orchestrator import step3_summarize
        result = step3_summarize({"topic": "K8s", "info": "facts", "analysis": "insight", "summary": ""})
        assert result["summary"] == "K8s simplifies deployment."


# ── choreography ───────────────────────────────────────────
def test_choreography_publish_and_consume():
    import coordination.choreography as choreo
    choreo.event_bus.clear()
    choreo.publish("task_created", "analyze sales")
    payload = choreo.consume("task_created")
    assert payload == "analyze sales"


def test_choreography_consume_returns_none_when_empty():
    import coordination.choreography as choreo
    choreo.event_bus.clear()
    assert choreo.consume("nonexistent_event") is None


# ── peer_to_peer_delegation ────────────────────────────────
def test_discover_agent_finds_pdf_agent():
    from coordination.peer_to_peer_delegation import discover_agent
    peer = discover_agent("pdf_analysis")
    assert peer is not None
    assert peer["id"] == "agent_pdf_analyzer"


def test_discover_agent_returns_none_for_unknown():
    from coordination.peer_to_peer_delegation import discover_agent
    assert discover_agent("unknown_capability_xyz") is None


# ── group_chat ─────────────────────────────────────────────
def test_group_chat_thread_starts_with_input():
    from coordination.group_chat import GroupChat, maker_checker_manager
    chat = (
        GroupChat(manager=maker_checker_manager(), max_turns=6)
        .add("maker", lambda thread: "draft v1")
        .add("checker", lambda thread: "APPROVED: looks good")
    )
    thread = chat.run("write a refund policy")
    assert thread[0] == ("input", "write a refund policy")


def test_group_chat_maker_checker_stops_on_approval():
    from coordination.group_chat import GroupChat, maker_checker_manager
    chat = (
        GroupChat(manager=maker_checker_manager(), max_turns=10)
        .add("maker", lambda thread: "draft v1")
        .add("checker", lambda thread: "APPROVED: done")
    )
    thread = chat.run("task")
    assert thread[-1][0] == "checker"
    assert "APPROVED" in thread[-1][1]


def test_group_chat_iteration_cap_bounds_loop():
    from coordination.group_chat import GroupChat, maker_checker_manager
    chat = (
        GroupChat(manager=maker_checker_manager(), max_turns=4)
        .add("maker", lambda thread: "draft")
        .add("checker", lambda thread: "REJECTED: not good enough")
    )
    thread = chat.run("x")
    assert len(thread) == 1 + 4  # input + max_turns


# ── magentic ───────────────────────────────────────────────
def test_magentic_clean_completion():
    from coordination.magentic import MagenticManager, TaskLedger

    def planner(ledger: TaskLedger) -> list[str]:
        done = {s for s, _ in ledger.done}
        if "researcher: market" not in done:
            return ["researcher: market"]
        if "writer: analysis" not in done:
            return ["writer: analysis"]
        return []

    mgr = (
        MagenticManager(planner=planner, max_rounds=8, stall_limit=2)
        .register("researcher", lambda t: f"found info on {t}")
        .register("writer", lambda t: f"wrote section: {t}")
    )
    ledger = mgr.run("competitive analysis")
    assert len(ledger.done) == 2
    assert ledger.open_questions == []


def test_magentic_stall_detection():
    from coordination.magentic import MagenticManager, TaskLedger

    mgr = MagenticManager(
        planner=lambda l: ["ghost: do something"],
        max_rounds=10,
        stall_limit=2,
    )
    ledger = mgr.run("impossible")
    assert any("stalled" in q for q in ledger.open_questions)
    assert len(ledger.done) == 0


def test_magentic_round_cap():
    from coordination.magentic import MagenticManager, TaskLedger
    calls = {"n": 0}

    def worker(t: str) -> str:
        calls["n"] += 1
        return "ok"

    mgr = (
        MagenticManager(planner=lambda l: ["worker: step"], max_rounds=3, stall_limit=99)
        .register("worker", worker)
    )
    ledger = mgr.run("endless")
    assert calls["n"] == 3
    assert any("round cap" in q for q in ledger.open_questions)


# ── mediator ───────────────────────────────────────────────
def test_mediator_routes_to_registered_agents():
    from coordination.mediator import MediatorAgent
    log = []
    def agent_a(task, ctx): log.append("a"); return "response_a"
    def agent_b(task, ctx): log.append("b"); return "response_b"
    mediator = MediatorAgent(max_rounds=2).register("a", agent_a).register("b", agent_b)
    mediator.coordinate("test goal")
    assert "a" in log and "b" in log


def test_mediator_context_accumulates():
    from coordination.mediator import MediatorAgent
    mediator = MediatorAgent(max_rounds=1)
    mediator.register("worker", lambda task, ctx: f"done:{len(ctx)}")
    mediator.coordinate("goal")
    assert len(mediator.context) >= 2  # goal + worker response


def test_mediator_single_send():
    from coordination.mediator import MediatorAgent
    mediator = MediatorAgent()
    mediator.register("echo", lambda task, ctx: f"echo:{task}")
    response = mediator.send(to="echo", content="hello")
    assert response == "echo:hello"


# ── saga ───────────────────────────────────────────────────
def test_saga_success_no_compensation():
    from coordination.saga import Saga
    log = []
    def step1(ctx): log.append("s1"); return {"s1": True}
    def comp1(out): log.append("c1")
    def step2(ctx): log.append("s2"); return {"s2": True}
    def comp2(out): log.append("c2")
    result = Saga().step("s1", step1, comp1).step("s2", step2, comp2).execute({})
    assert result.success
    assert result.compensated == []
    assert "c1" not in log and "c2" not in log


def test_saga_failure_triggers_reverse_compensation():
    from coordination.saga import Saga
    log = []
    def step1(ctx): log.append("s1"); return {}
    def comp1(out): log.append("c1")
    def step2(ctx): log.append("s2"); raise RuntimeError("oops")
    def comp2(out): log.append("c2")
    result = Saga().step("s1", step1, comp1).step("s2", step2, comp2).execute({})
    assert not result.success
    assert result.failed_at == "s2"
    assert "c1" in log
    assert "c2" not in log


def test_saga_records_completed_steps():
    from coordination.saga import Saga
    def ok(ctx): return {}
    def noop(out): pass
    def fail(ctx): raise ValueError("boom")
    result = Saga().step("a", ok, noop).step("b", ok, noop).step("c", fail, noop).execute({})
    assert result.completed == ["a", "b"]
    assert result.failed_at == "c"
