# Direct Message

> Send a task from one agent to exactly one other agent through a dedicated point-to-point channel.

**Category:** messaging
**EIP Analog:** [Point-to-Point Channel](https://www.enterpriseintegrationpatterns.com/patterns/messaging/PointToPointChannel.html)

---

## Also Known As

Task Delegation, A2A Task Request, Agent Handoff

---

## Problem

An agent needs to delegate a specific subtask to another agent with known capabilities. Broadcasting to all agents wastes resources, and the sender needs a reliable response — not just fire-and-forget.

---

## Solution

Establish a dedicated channel between two agents. The sender pushes a structured message (task + context) to the receiver's endpoint. The receiver acknowledges receipt, processes the task, and returns a result. The channel is exclusive to this sender-receiver pair for the duration of the task.

---

## Diagram

```
┌──────────┐    Task Request    ┌──────────┐
│ Agent A  │ ─────────────────► │ Agent B  │
│ (sender) │                   │(receiver)│
│          │ ◄───────────────── │          │
└──────────┘    Task Result     └──────────┘
```

---

## Participants

| Participant | Role |
|---|---|
| **Sender Agent** | Initiates the task; holds context about what needs to be done |
| **Receiver Agent** | Accepts the task, executes it, returns a structured result |
| **Channel** | The transport: A2A HTTP endpoint, LangGraph edge, or direct function call |

---

## Consequences

**Benefits:**
- ✅ Simple, predictable, and easy to trace in logs
- ✅ Low latency — no intermediary broker required
- ✅ Result is returned synchronously or via callback; no polling needed

**Trade-offs:**
- ❌ Tight coupling — sender must know the receiver's address or identity
- ❌ No built-in load balancing or failover without additional infrastructure
- ❌ If the receiver is down, the sender must handle the failure explicitly

---

## Implementation

```python
# A2A-style direct task delegation using the A2A Python client
from a2a.client import A2AClient
from a2a.types import SendTaskRequest, TaskState

async def delegate_pdf_extraction(pdf_url: str) -> str:
    client = A2AClient(url="https://agents.example.com/extractor")

    request = SendTaskRequest(
        id="task-001",
        message={
            "role": "user",
            "parts": [{"type": "text", "text": f"Extract text from: {pdf_url}"}],
        },
    )

    response = await client.send_task(request)

    if response.result.status.state == TaskState.completed:
        return response.result.status.message.parts[0].text
    else:
        raise RuntimeError(f"Task failed: {response.result.status.message}")
```

---

## Known Uses

- **Google A2A Protocol** — the primary mechanism for agent-to-agent task delegation; each task is a Direct Message to a specific Agent Card endpoint
- **LangGraph node edges** — edges between nodes in a StateGraph are point-to-point: output of node A flows to node B and nowhere else
- **ReAct agents (tool calls)** — when an agent invokes a tool, the tool call is a direct message to that tool's handler

---

## Related Patterns

- [Agent Card Registry](../discovery/agent-card-registry.md) — use before this pattern to discover the receiver's address
- [Supervised Delegation](../coordination/supervised-delegation.md) — wraps Direct Message with monitoring and retry
- [Scatter-Gather](../routing/scatter-gather.md) — sends the same message to multiple receivers instead of one

---

## References

- [A2A Protocol Specification](https://a2a-protocol.org/specification/latest/Agent-to-Agent%20Protocol%20Specification)
- Hohpe & Woolf (2003). *Enterprise Integration Patterns*, Chapter 3: Point-to-Point Channel
