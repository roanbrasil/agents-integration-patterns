# Peer-to-Peer Delegation

> An agent directly delegates a subtask to another agent through a capability-negotiated channel, without involving a central coordinator.

**Category:** coordination
**EIP Analog:** [Messaging Gateway](https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessagingGateway.html) (dynamic variant)

---

## Also Known As

A2A Delegation, Dynamic Handoff, Autonomous Task Transfer

---

## Problem

An agent discovers mid-execution that a subtask requires capabilities it does not possess. A central coordinator may not exist, may be unavailable, or the delegation decision can only be made with context available locally to the delegating agent. The agent needs to find and delegate to a capable peer autonomously.

---

## Solution

Using Agent Card discovery, the delegating agent queries the registry for an agent with the required capability. It establishes an A2A channel directly with the discovered peer, sends the task with relevant context, and awaits the result. The delegating agent resumes its own work once the result is received — no coordinator involved.

---

## Diagram

![Peer-to-Peer Delegation — Agent A discovers Agent B via Agent Registry, sends A2A Task Request, receives A2A Task Result without a central coordinator](../../img/peer-to-peer-delegation-a2a.png)

---

## Participants

| Participant | Role |
|---|---|
| **Delegating Agent** | Identifies the need, discovers the peer, delegates, awaits result |
| **Agent Registry** | Resolves capability queries to agent endpoints |
| **Peer Agent** | Receives the delegated task, executes it, returns the result |

---

## Consequences

**Benefits:**
- ✅ No coordinator bottleneck — delegation scales horizontally
- ✅ Agents remain autonomous; composition happens at runtime based on actual needs
- ✅ Works across framework boundaries (LangGraph agent can delegate to an AutoGen agent via A2A)

**Trade-offs:**
- ❌ Discovery overhead per delegation adds latency
- ❌ Trust must be established between every agent pair at runtime
- ❌ Debugging delegations across agents requires distributed tracing

---

## Implementation

```python
# Peer-to-peer delegation using the A2A Python client
import httpx
from a2a.client import A2AClient
from a2a.types import SendTaskRequest

async def discover_and_delegate(capability: str, task_text: str) -> str:
    # Step 1: discover peer with needed capability
    async with httpx.AsyncClient() as http:
        resp = await http.get(
            "https://registry.example.com/agents",
            params={"skill": capability},
        )
        peer_url = resp.json()[0]["url"]

    # Step 2: fetch Agent Card to verify capability and get auth info
    peer_card = await http.get(f"{peer_url}/.well-known/agent.json")

    # Step 3: delegate via A2A
    client = A2AClient(url=peer_url)
    request = SendTaskRequest(
        id=f"delegated-{capability}-001",
        message={
            "role": "user",
            "parts": [{"type": "text", "text": task_text}],
        },
    )

    response = await client.send_task(request)
    return response.result.status.message.parts[0].text


# Usage inside a larger agent
async def main_agent_task(document_url: str):
    # Main agent realizes it needs OCR mid-task
    ocr_result = await discover_and_delegate(
        capability="pdf-ocr",
        task_text=f"Extract text from PDF at: {document_url}",
    )
    # Continue with the OCR result
    return analyze_text(ocr_result)
```

---

## Known Uses

- **Google A2A Protocol** — the primary use case for A2A is peer-to-peer delegation: agents delegate to other A2A-compliant agents discovered via Agent Cards
- **Salesforce Agentforce** — agents in Agentforce flows can delegate sub-tasks to specialized agents in the same ecosystem
- **Spring AI multi-agent flows** — Spring AI supports A2A delegation between independently deployed Spring AI agents

---

## Related Patterns

- [Agent Card Registry](../discovery/agent-card-registry.md) — required for peer discovery; must be running before this pattern can work
- [Supervised Delegation](./supervised-delegation.md) — use instead when a supervisor should control and monitor all delegations
- [Trust Boundary](../security/trust-boundary.md) — establish trust tiers between agents before allowing peer-to-peer delegation

---

## References

- [A2A Protocol Specification](https://a2a-protocol.org/specification/latest/Agent-to-Agent%20Protocol%20Specification)
- [Google Developer Blog: A2A Launch](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- arXiv:2501.06322 — peer-to-peer structure is one of three primary coordination structures in multi-agent LLM systems
