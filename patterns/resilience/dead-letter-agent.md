# Dead Letter Agent
**Category:** Resilience
**Maturity:** ★★ Established
**Also known as:** Dead Letter Queue, Error Handler, Fallback Agent

> Route tasks that cannot be processed to a dedicated agent or human for inspection and resolution.

**EIP Analog:** [Dead Letter Channel](https://www.enterpriseintegrationpatterns.com/patterns/messaging/DeadLetterChannel.html)

---

## Intent

Route tasks that cannot be processed — after retries and circuit breaking — to a dedicated handler that ensures no failure is silently dropped.

---

## Context

In any agent system, some tasks will fail: the model refuses, the tool errors out, the task is malformed, or the confidence is too low to proceed.

---

## Problem

Without a safety net, failed tasks are silently dropped, leaving users without responses and operators without visibility into what went wrong or how often.

---

## Forces

- **F4 Reliability** — no silent data loss; every failed task has a handler.
- **F6 Observability** — dead letter volume is a system health signal; high volume indicates a systemic issue upstream.
- **F11 Operational complexity** — requires monitoring the dead letter handler; without human attention, it becomes a black hole.

---

## Solution

Any task that cannot be processed — after retries, after circuit breaking — is forwarded to a Dead Letter Agent. This agent may route to a human review queue, send an alert, log the failure for audit, or attempt a last-resort strategy (e.g., ask the user to clarify). The dead letter agent never loses the failed task.

---

## Diagram

![Dead Letter Agent — Agent A failure is routed to the Dead Letter Agent, which triggers Human review / alert](../../img/dead-letter-agent.png)

---

## Participants

| Participant | Role |
|---|---|
| **Failed Agent** | Detects it cannot process the task and forwards to the dead letter agent |
| **Dead Letter Agent** | Receives unprocessable tasks; routes to human review, alerts, or audit |
| **Human Reviewer** | Inspects failed tasks; may manually complete, retry, or discard |
| **Audit Log** | Permanent record of all failures for post-hoc analysis |

---

## Sample Code

Runnable implementation: [samples/python/resilience/dead_letter_agent.py](../../samples/python/resilience/dead_letter_agent.py)

```python
# Dead Letter Agent with LangGraph interrupt
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict

class TaskState(TypedDict):
    task: str
    result: str | None
    error: str | None
    retry_count: int

def process_agent(state: TaskState) -> TaskState:
    try:
        result = risky_operation(state["task"])
        return {"result": result}
    except Exception as e:
        return {"error": str(e), "retry_count": state.get("retry_count", 0) + 1}

def route_after_processing(state: TaskState) -> str:
    if state.get("result"):
        return "done"
    if state.get("retry_count", 0) < 2:
        return "retry"
    return "dead_letter"

def dead_letter_agent(state: TaskState) -> TaskState:
    # Persist to audit log
    log_failure(task=state["task"], error=state["error"])
    # Notify human reviewer
    send_alert(f"Task failed after retries: {state['task']}\nError: {state['error']}")
    # Interrupt: wait for human intervention via LangGraph's interrupt mechanism
    return state  # human can inject a corrected task via update_state()

graph = StateGraph(TaskState)
graph.add_node("process", process_agent)
graph.add_node("dead_letter", dead_letter_agent)
graph.add_conditional_edges("process", route_after_processing,
    {"done": END, "retry": "process", "dead_letter": "dead_letter"})
graph.add_edge("dead_letter", END)
```

---

## Consequences

- ✅ No silent data loss (F4 resolved)
- ✅ Human-in-the-loop safety net
- ✅ Dead letter volume is a free health metric (F6 resolved)
- ❌ Requires monitoring and human attention
- ❌ Does not fix the upstream failure that sent the task here

---

## When to avoid

- When every task is idempotent and retry is sufficient — a dead letter agent adds infrastructure without value.
- When tasks can safely be dropped (rare; document this decision explicitly).

---

## Failure Modes Mitigated

Per [FAILURE-MAP.md](../FAILURE-MAP.md):
- **FM-3.2 No or incomplete verification** ◐ — failed tasks are not silently dropped; they are routed to a handler for inspection.
- **FM-2.2 Fail to ask for clarification** ◐ — the dead letter handler can escalate to a human who can clarify and resubmit.

---

## Known Uses

- **LangGraph `interrupt()`** — pauses agent execution at a node and waits for human input; the canonical implementation of human-in-the-loop dead letter handling
- **Anthropic's Agent Cookbook** — recommends human-in-the-loop as the explicit fallback for irreversible or high-stakes actions
- **CrewAI Human Input Tool** — tasks that agents cannot complete autonomously are escalated to a human via the `human_input=True` flag

---

## Related Patterns

- *used-by* [Ensemble Judge](../evaluation/ensemble-judge.md) — rejected outputs after max retries route to dead letter.
- *used-by* [Group Chat](../coordination/group-chat.md) — tasks that exceed the iteration cap escalate here.
- *used-by* [Magentic Orchestration](../coordination/magentic.md) — stall escalation target.
- *complements* [Circuit Breaker](circuit-breaker.md) — circuit breaker prevents calls; dead letter handles the ones that got through and failed.

---

## References

- Hohpe, G. & Woolf, B. (2003). *Enterprise Integration Patterns* — Dead Letter Channel.
- Cemri, M. et al. (2025). arXiv:2503.13657.
- [Anthropic: Human-in-the-Loop Patterns](https://www.anthropic.com/research/building-effective-agents)
- [LangGraph: How to Add Human-in-the-Loop](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/)
