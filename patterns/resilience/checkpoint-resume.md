# Checkpoint & Resume
**Category:** Resilience
**Maturity:** ★★ Established
**Also known as:** State Persistence, Saga Checkpoint, Workflow Resume

> Persist intermediate agent state so that long-running tasks can be paused and resumed without restarting from scratch.

**EIP Analog:** No direct EIP analog — closest to durable execution patterns (Temporal, AWS Step Functions)

---

## Intent

After each significant step, serialize agent state to a durable store so that failures, restarts, or human interruptions resume from the last checkpoint rather than from the beginning.

---

## Context

Long agent workflows run for minutes or hours and involve expensive LLM calls, tool executions, and accumulated context.

---

## Problem

A network failure, context window exhaustion, cost budget hit, or required human review can interrupt execution. Restarting from zero wastes resources, time, and can produce inconsistent results.

---

## Forces

- **F8 Determinism / Reproducibility** — checkpointed state enables exact resume from the last successful step; no work is repeated unnecessarily.
- **F4 Reliability** — long-running workflows survive transient failures, infrastructure restarts, and rate limit errors.
- **F11 Operational complexity** — checkpointing requires a durable store (database, object storage); adds infrastructure.
- **F3 Token cost** — without checkpoints, a failure near the end of a 50-step pipeline reruns everything from step 1.

---

## Solution

After each significant step, serialize the agent's full state — task progress, accumulated results, intermediate context, memory — to a durable store. On failure or interruption, load the last checkpoint and resume execution from that point. The checkpoint boundary is also a natural point for human review or approval before proceeding.

---

## Diagram

![Checkpoint & Resume — Step 1 → [Checkpoint] → Step 2 → [Checkpoint] → Step 3, with arrow showing resume from checkpoint on failure](../../img/checkpoint-and-resume.png)

---

## Participants

| Participant | Role |
|---|---|
| **Agent / Workflow** | Executes steps; signals the checkpoint layer after each significant step |
| **Checkpoint Store** | Durable storage for serialized state (SQLite, Postgres, Redis, S3) |
| **Resume Logic** | Loads the latest checkpoint and restores execution context |
| **Human Reviewer** *(optional)* | May inspect and approve state at a checkpoint before the next step runs |

---

## Sample Code

Runnable implementation: [samples/python/resilience/checkpoint_resume.py](../../samples/python/resilience/checkpoint_resume.py)

```python
# LangGraph with Postgres checkpointer
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver
from typing import TypedDict
import psycopg

class ResearchState(TypedDict):
    topic: str
    sources: list[str]
    draft: str
    reviewed: bool

def gather_sources(state: ResearchState) -> ResearchState:
    # Expensive operation — checkpoint after this
    sources = search_web(state["topic"], limit=20)
    return {"sources": sources}

def write_draft(state: ResearchState) -> ResearchState:
    draft = llm_write(state["sources"])
    return {"draft": draft}

def human_review(state: ResearchState) -> ResearchState:
    # Interrupt here — human reviews and approves via update_state()
    return state

graph = StateGraph(ResearchState)
graph.add_node("gather", gather_sources)
graph.add_node("draft", write_draft)
graph.add_node("review", human_review)  # checkpoint + human interrupt

graph.set_entry_point("gather")
graph.add_edge("gather", "draft")
graph.add_edge("draft", "review")
graph.add_edge("review", END)

# Postgres checkpointer — survives process restart
conn = psycopg.connect("postgresql://localhost/agents")
checkpointer = PostgresSaver(conn)
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["review"],  # pause before human review node
)

# Resume a workflow by thread_id
config = {"configurable": {"thread_id": "research-task-001"}}
result = await app.ainvoke({"topic": "AI agents"}, config=config)
# After crash: same thread_id resumes from last checkpoint automatically
```

---

## Consequences

- ✅ Long workflows survive failures — resume from last checkpoint (F8, F4 resolved)
- ✅ Token cost savings on retry — only failed steps re-run (F3 resolved)
- ❌ Requires durable checkpoint store (F11 introduced)
- ❌ Checkpointing adds latency per step

---

## When to avoid

- When workflows are short and cheap to retry from scratch.
- When idempotency cannot be guaranteed — resuming a non-idempotent step can cause duplicate effects.

---

## Failure Modes Mitigated

Per [FAILURE-MAP.md](../FAILURE-MAP.md):
- **FM-2.1 Conversation reset** ✅ — checkpointed state means a restart resumes from the last good state, not from scratch.
- **FM-1.3 Step repetition** ✅ — the checkpoint record shows which steps are done; completed steps are not re-run.
- **FM-1.4 Loss of context** ✅ — context accumulated across steps is persisted in the checkpoint, not held only in memory.

---

## Known Uses

- **LangGraph checkpointers** — built-in SQLite, Postgres, and Redis checkpointers; each StateGraph step is automatically checkpointed; threads resume by ID
- **12-Factor Agents — "Own your control flow"** — factor 9 explicitly recommends checkpointing as essential for production agents
- **AWS Step Functions** — each state machine step is durably persisted; execution can resume from any step after failure
- **Temporal** — workflow history provides automatic checkpointing; workers can restart anywhere in the workflow history

---

## Related Patterns

- *used-by* [Orchestrator](../coordination/orchestrator.md) — centralized state is what makes checkpointing natural.
- *used-by* [Magentic Orchestration](../coordination/magentic.md) — the task ledger is a natural checkpoint boundary.
- *complements* [Pipeline](../routing/pipeline.md) — pipeline steps are natural checkpoint boundaries.
- *used-by* [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) — "own your control flow" factor.

---

## References

- Hohpe, G. & Woolf, B. (2003). *Enterprise Integration Patterns* — Process Manager with persistent state.
- HumanLayer (2025). *12-Factor Agents.*
- Cemri, M. et al. (2025). arXiv:2503.13657.
- [LangGraph Persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/)
- [12-Factor Agents: Factor 9 — Own your control flow](https://github.com/humanlayer/12-factor-agents)
- [Temporal: Durable Execution](https://docs.temporal.io/concepts/what-is-a-workflow)
