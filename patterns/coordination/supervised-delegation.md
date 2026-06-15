# Supervised Delegation

> A supervisor agent decomposes a goal into subtasks, delegates each to a specialist agent, monitors execution, and intervenes on failure.

**Category:** coordination
**EIP Analog:** [Process Manager](https://www.enterpriseintegrationpatterns.com/patterns/messaging/ProcessManager.html)

---

## Also Known As

Supervisor-Worker, Manager-Agent, Hierarchical Delegation

---

## Problem

Complex goals exceed any single agent's capacity and benefit from specialization. But tasks need to be distributed while the overall goal remains coherent — failures in subtasks must be handled, retried, or escalated without losing the global state.

---

## Solution

A supervisor agent owns the high-level goal and maintains a plan. It decomposes the goal into subtasks, assigns each to a specialist worker agent, and monitors their execution. When a worker fails, the supervisor retries with the same or a different agent, adjusts the plan, or escalates to a human. The supervisor never executes domain tasks itself.

---

## Diagram

![Supervised Delegation — Supervisor Agent monitors and guides Worker A, B, and C agents, each performing assigned tasks under supervision](../../img/Supervised-Delegation.png)

---

## Participants

| Participant | Role |
|---|---|
| **Supervisor Agent** | Decomposes goals, assigns tasks, monitors workers, handles failures |
| **Worker Agents** | Execute assigned subtasks; report results or failures to the supervisor |
| **Human Escalation** | Receives tasks the supervisor cannot resolve autonomously |

---

## Consequences

**Benefits:**
- ✅ Clear accountability — supervisor owns the goal end-to-end
- ✅ Fault tolerance — supervisor can retry, reassign, or restructure the plan on failure
- ✅ Workers stay focused on their domain; the supervisor handles coordination complexity

**Trade-offs:**
- ❌ Supervisor is a single point of failure and bottleneck
- ❌ Supervisor quality (LLM quality + prompt quality) determines overall system quality
- ❌ Requires careful prompt design to avoid infinite retry loops

---

## Implementation

```python
# LangGraph Supervisor pattern
from langgraph.graph import StateGraph, END
from langgraph_supervisor import create_supervisor
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-6")

# Define worker agents
from langchain_core.tools import tool

@tool
def research_topic(topic: str) -> str:
    """Research a topic and return findings."""
    return f"Research findings for: {topic}"

@tool
def write_section(content: str, section: str) -> str:
    """Write a report section based on content."""
    return f"Section '{section}' written with content: {content[:100]}..."

# Supervisor routes between workers and synthesizes
supervisor = create_supervisor(
    llm=llm,
    agents=["researcher", "writer"],
    prompt=(
        "You are a supervisor coordinating a research report. "
        "First have the researcher gather information, then have the writer produce sections. "
        "If a worker fails, retry once before escalating."
    ),
)
```

---

## Known Uses

- **AWS Bedrock Multi-Agent Supervisor** — a dedicated supervisor agent decomposes requests and routes to registered sub-agents, monitoring completion and handling errors
- **AutoGen GroupChatManager** — orchestrates agent conversations, decides who speaks next, and handles termination conditions
- **LangGraph Supervisor Pattern** — documented pattern using conditional edges from a supervisor node to worker nodes

---

## Related Patterns

- [Orchestrator](./orchestrator.md) — lighter-weight coordination without runtime monitoring; use when the workflow is well-defined and failures are handled by retry policies
- [Dead Letter Agent](../resilience/dead-letter-agent.md) — the escalation target when the supervisor cannot resolve a failure
- [Circuit Breaker](../resilience/circuit-breaker.md) — protect the supervisor from repeatedly calling a failing worker

---

## References

- Hohpe & Woolf (2003). *Enterprise Integration Patterns*: Process Manager
- [LangGraph Supervisor Tutorial](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/)
- arXiv:2501.06322 — classifies hierarchical structures as a primary multi-agent coordination dimension
