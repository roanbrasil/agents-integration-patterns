# Checkpoint & Resume

> Persist intermediate agent state so that long-running tasks can be paused and resumed without restarting from scratch.

**Category:** resilience
**EIP Analog:** No direct EIP analog — closest to durable execution patterns (Temporal, AWS Step Functions)

---

## Also Known As

Durable Execution, State Persistence, Workflow Resumption

---

## Problem

Long agent workflows run for minutes or hours and involve expensive LLM calls, tool executions, and accumulated context. A network failure, context window exhaustion, cost budget hit, or required human review can interrupt execution. Restarting from zero wastes resources, time, and can produce inconsistent results.

---

## Solution

After each significant step, serialize the agent's full state — task progress, accumulated results, intermediate context, memory — to a durable store. On failure or interruption, load the last checkpoint and resume execution from that point. The checkpoint boundary is also a natural point for human review or approval before proceeding.

---

## Diagram

```
 Step 1 ──► [Checkpoint] ──► Step 2 ──► [Checkpoint] ──► Step 3
    ✓             ✓              ✓              ✓
                                         ▲
                                (crash/pause here)
                                         │
                                   [Resume from
                                    Checkpoint 2]
```

---

## Participants

| Participant | Role |
|---|---|
| **Agent / Workflow** | Executes steps; signals the checkpoint layer after each significant step |
| **Checkpoint Store** | Durable storage for serialized state (SQLite, Postgres, Redis, S3) |
| **Resume Logic** | Loads the latest checkpoint and restores execution context |
| **Human Reviewer** *(optional)* | May inspect and approve state at a checkpoint before the next step runs |

---

## Consequences

**Benefits:**
- ✅ Survives network failures, process crashes, and context window resets
- ✅ Enables human-in-the-loop review at defined points without losing progress
- ✅ Reduces cost on failure — resume from the last step, not the beginning

**Trade-offs:**
- ❌ Checkpoint storage and schema versioning add operational complexity
- ❌ Non-idempotent operations (e.g., sending an email) may be duplicated on resume
- ❌ State serialization can be large for long workflows with large context

---

## Implementation

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

## Known Uses

- **LangGraph checkpointers** — built-in SQLite, Postgres, and Redis checkpointers; each StateGraph step is automatically checkpointed; threads resume by ID
- **12-Factor Agents — "Own your control flow"** — factor 9 explicitly recommends checkpointing as essential for production agents
- **AWS Step Functions** — each state machine step is durably persisted; execution can resume from any step after failure
- **Temporal** — workflow history provides automatic checkpointing; workers can restart anywhere in the workflow history

---

## Related Patterns

- [Dead Letter Agent](./dead-letter-agent.md) — after max retries, forward the checkpointed state to the dead letter agent for human review
- [Orchestrator](../coordination/orchestrator.md) — the orchestrator's state is what gets checkpointed
- [Supervised Delegation](../coordination/supervised-delegation.md) — supervisor state (task assignments, results) should be checkpointed

---

## References

- [LangGraph Persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/)
- [12-Factor Agents: Factor 9 — Own your control flow](https://github.com/humanlayer/12-factor-agents)
- [Temporal: Durable Execution](https://docs.temporal.io/concepts/what-is-a-workflow)
