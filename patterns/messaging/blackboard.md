# Blackboard
**Category:** Messaging
**Maturity:** ★★ Established
**Also known as:** Shared Context, Shared Memory, Tuple Space, Working Memory

> Share a structured, mutable context space that multiple agents read from and write to asynchronously.

**EIP Analog:** [Shared Database](https://www.enterpriseintegrationpatterns.com/patterns/messaging/SharedDataBase.html) (extended for agent-specific concerns)

---

## Intent

Share a structured, mutable context space that multiple agents read from and write to asynchronously, eliminating point-to-point coupling while making accumulated knowledge visible to every participant.

---

## Context

Multiple specialized agents work on different facets of the same problem. No single agent has the full picture, but each agent's output becomes input for others. Coordinating this through direct messaging or a central router creates either N² connections or a bottleneck.

---

## Problem

Multiple agents work on different parts of the same problem. No single agent has the full picture, but they all need to read each other's intermediate results. Point-to-point messaging between every pair of agents is impractical (N² connections). A central coordinator that routes every message is a bottleneck.

---

## Forces
- **F2 Coupling** — agents do not address each other directly; they only read and write the shared store.
- **F9 Scalability** — agents contribute at their own pace; no synchronization required between agents.
- **F6 Observability** — the full shared state is inspectable at any point.
- **F11 Operational complexity** — requires conflict resolution when agents write the same key; partitioning the namespace reduces this.

---

## Solution

Maintain a shared "blackboard" — a structured key-value store or document that acts as the shared workspace. Agents read state relevant to their role, contribute their results by writing to the blackboard, and optionally observe changes via subscriptions. An optional controller monitors the blackboard and triggers agents when their preconditions are met.

---

## Diagram

![Blackboard — shared context space with Agent A, B, and C all reading and writing](../../img/blackboard-shared-context.png)

---

## Participants

| Participant | Role |
|---|---|
| **Blackboard** | The shared, structured context store |
| **Knowledge Sources (Agents)** | Specialized agents that read relevant state, execute, and write results |
| **Controller** *(optional)* | Monitors the blackboard and activates agents when their preconditions are satisfied |

---

## Sample Code
Runnable implementation: [samples/python/messaging/blackboard.py](../../samples/python/messaging/blackboard.py)

```python
# Blackboard using LangGraph shared state
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
import operator

class BlackboardState(TypedDict):
    query: str
    web_results: Annotated[list, operator.add]   # Agent A writes here
    db_results: Annotated[list, operator.add]    # Agent B writes here
    synthesis: str                               # Agent C reads both, writes here

def web_search_agent(state: BlackboardState):
    results = search_web(state["query"])
    return {"web_results": results}   # writes to blackboard

def db_query_agent(state: BlackboardState):
    results = query_database(state["query"])
    return {"db_results": results}    # writes to blackboard

def synthesis_agent(state: BlackboardState):
    # reads from blackboard — sees results from both agents
    combined = state["web_results"] + state["db_results"]
    return {"synthesis": summarize(combined)}

graph = StateGraph(BlackboardState)
graph.add_node("web", web_search_agent)
graph.add_node("db", db_query_agent)
graph.add_node("synthesize", synthesis_agent)
```

---

## Consequences
- ✅ Natural for parallel, loosely-coupled agents (F2, F9 resolved)
- ✅ Agents contribute at their own pace
- ✅ Full state inspectable at any point (F6 resolved)
- ❌ Requires conflict resolution when agents write same key (F11 introduced)
- ❌ Stale reads if an agent caches the blackboard snapshot

---

## When to avoid
- When agents need to react to each other in real time — use [Group Chat](../coordination/group-chat.md) instead.
- When strong write ordering is required — use a Pipeline.
- When the problem is strictly sequential — use [Pipeline](../routing/pipeline.md).

---

## Failure Modes Mitigated
Per [FAILURE-MAP.md](../FAILURE-MAP.md):
- **FM-1.4 Loss of conversation history / context** ✅ — shared state persists across all agent turns; no agent can lose the accumulated context.
- **FM-2.4 Information withholding** ✅ — all agents read the full blackboard; information is structurally shared, not siloed per agent.
- **FM-2.1 Conversation reset** ◐ — the blackboard is not a conversation log, but key-value persistence mitigates partial context loss.

---

## Known Uses

- **LangGraph StateGraph** — the `State` object is a blackboard shared across all nodes in the graph
- **AutoGen shared memory** — agents in a conversation share a common message history as the blackboard
- **Multi-agent RAG systems** — a shared document store where retrieval agents write chunks and synthesis agents read them

---

## Related Patterns
- *alternative-to* [Group Chat](../coordination/group-chat.md) — shared mutable state rather than a conversation thread.
- *complements* [Checkpoint & Resume](../resilience/checkpoint-resume.md) — the blackboard is a natural checkpoint target.
- *complements* [Broadcast Message](broadcast-message.md) — broadcast pushes events; blackboard stores accumulated state.

---

## References
- Buschmann, F. et al. (1996). *Pattern-Oriented Software Architecture* (POSA1) — Blackboard.
- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv:2503.13657.
- Corkill, D.D. (1991). "Blackboard Systems." *AI Expert*, 6(9):40-47.
- arXiv:2502.14321 — classifies Blackboard as one of three primary communication paradigms in LLM multi-agent systems
