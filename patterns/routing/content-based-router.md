# Content-Based Router
**Category:** Routing
**Maturity:** ★★ Established
**Also known as:** Task Router, Triage Agent, Dispatch Agent, Handoff

> Route an incoming task to the appropriate agent based on the content, type, or intent of the task itself.

**EIP Analog:** [Content-Based Router](https://www.enterpriseintegrationpatterns.com/patterns/messaging/ContentBasedRouter.html)

---

## Intent

A system receives diverse tasks that require different specialized agents. A caller should not need to know which agent handles which type of task — that's an implementation detail. But you need a principled way to route each task to the right specialist without a central human deciding for each request.

---

## Context

Multi-agent systems expose a single entry point to callers but internally route work to specialists. As the number of task types grows, a routing layer becomes essential to preserve encapsulation and enable independent evolution of specialists.

---

## Problem

A system receives diverse tasks that require different specialized agents. A caller should not need to know which agent handles which type of task — that's an implementation detail. But you need a principled way to route each task to the right specialist without a central human deciding for each request.

---

## Forces

- **F4 Answer quality** — routing to the right specialist dramatically improves quality vs. a generalist handling everything.
- **F1 Latency** — classification adds a router step before the specialist call; usually worth it when specialist quality gain is large.
- **F10 Adaptability** — new specializations can be added by registering new routes without modifying existing agents.
- **F6 Observability** — routing decisions are explicit and loggable, making flow visible.

---

## Solution

A router agent examines the content, metadata, or intent of each incoming task and forwards it to the appropriate specialist. The router may use: LLM-based intent classification (flexible, handles ambiguous input), rule-based matching (fast, deterministic for well-defined categories), or embedding similarity (good for semantic matching across many agents).

---

## Diagram

![Content-Based Router — Incoming Task flows into Router Agent (LLM classifier or rule engine), which routes to Coding Agent, Research Agent, or Data Agent](../../img/content-based-router.png)

---

## Participants

| Participant | Role |
|---|---|
| **Router Agent** | Classifies incoming tasks and forwards to the appropriate specialist |
| **Specialist Agents** | Handle tasks for their domain; unaware of the routing logic |
| **Classifier** | The classification mechanism inside the router (LLM prompt, rules, embeddings) |

---

## Sample Code

Runnable implementation: [samples/python/routing/content_based_router.py](../../samples/python/routing/content_based_router.py)

```python
# LLM-based intent router using LangGraph conditional edges
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")  # fast model for routing

class RouterState(TypedDict):
    task: str
    route: str
    result: str

def classify_task(state: RouterState) -> RouterState:
    response = llm.invoke(
        f"Classify this task as exactly one of: coding, research, data_analysis.\n"
        f"Task: {state['task']}\nAnswer with only the category name."
    )
    return {"route": response.content.strip()}

def route_decision(state: RouterState) -> Literal["coding", "research", "data_analysis"]:
    return state["route"]

def coding_agent(state: RouterState) -> RouterState:
    return {"result": f"[Code] handled: {state['task']}"}

def research_agent(state: RouterState) -> RouterState:
    return {"result": f"[Research] handled: {state['task']}"}

def data_agent(state: RouterState) -> RouterState:
    return {"result": f"[Data] handled: {state['task']}"}

graph = StateGraph(RouterState)
graph.add_node("router", classify_task)
graph.add_node("coding", coding_agent)
graph.add_node("research", research_agent)
graph.add_node("data_analysis", data_agent)

graph.set_entry_point("router")
graph.add_conditional_edges("router", route_decision)
for node in ["coding", "research", "data_analysis"]:
    graph.add_edge(node, END)
```

---

## Consequences

- ✅ Right specialist for each task type — quality improvement (F4 resolved)
- ✅ New routes addable without modifying existing agents (F10 resolved)
- ✅ Single entry point for callers — they don't need to know agent topology
- ❌ Router classification is a failure point — misclassification sends tasks to wrong agents
- ❌ Latency increases by one classification step (F1 introduced)
- ❌ Router is a bottleneck and single point of failure

---

## When to avoid

- When all tasks are similar enough that a generalist handles them as well as a specialist.
- When the classification itself is unreliable (the router adds error without adding value).

---

## Failure Modes Mitigated

Per [FAILURE-MAP.md](../FAILURE-MAP.md):
- **FM-1.2 Disobey role specification** ✅ — tasks reach agents that are registered for exactly that role.
- **FM-2.3 Task derailment** ✅ — off-topic tasks are routed away from specialists that would mishandle them.

---

## Known Uses

- **AWS Bedrock Supervisor Mode** — the supervisor agent classifies tasks and routes them to registered sub-agents based on their registered capabilities
- **LangGraph conditional edges** — `add_conditional_edges` implements content-based routing between graph nodes
- **Semantic Router (Aurelio AI)** — open-source library that uses embedding similarity to route LLM requests to different handlers

---

## Related Patterns

- *alternative-to* [Scatter-Gather](scatter-gather.md) — route to one vs. fan out to all.
- *uses* [Agent Card Registry](../discovery/agent-card-registry.md) — registry maps capability to agent address.
- *used-by* [Peer-to-Peer Delegation](../coordination/peer-to-peer-delegation.md) — P2P delegation uses content-based routing to find the right peer.

---

## References

- Hohpe, G. & Woolf, B. (2003). *Enterprise Integration Patterns* — Content-Based Router.
- Microsoft (2026). *AI Agent Orchestration Patterns* — Handoff.
- Cemri, M. et al. (2025). arXiv:2503.13657.
- [LangGraph Conditional Edges](https://langchain-ai.github.io/langgraph/concepts/low_level/#conditional-edges)
