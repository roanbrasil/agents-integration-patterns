# Mediator Agent
**Category:** Coordination
**Maturity:** ★ Emerging
**Also known as:** Interaction Broker, Central Coordinator, Hub Agent, Supervisor LLM

## Intent
Eliminate direct agent-to-agent dependencies by routing all inter-agent communication through a single mediator, reducing N² couplings to N and enabling centralized routing, context management, and conflict resolution.

## Context
You have N specialized agents that must collaborate: they share context, coordinate on sub-tasks, and must be aware of each other's progress. In a naive design, every agent that needs to communicate with others holds direct references — creating N² dependencies, duplicating context management, and making the system hard to change.

## Problem
As the number of collaborating agents grows, direct peer-to-peer communication creates an N²-coupling explosion: each new agent must integrate with every existing agent. Context must be duplicated or synchronized across pairs. Changing one agent's interface requires updating all its direct callers. Conflict resolution (two agents disagree on a fact) has no natural home.

## Forces
- **F2 Coupling** — this is the pattern's entire purpose: replace N² agent-to-agent links with N mediator-to-agent links. Adding a new agent costs O(1) integration (register with the mediator), not O(N).
- **F9 Scalability vs. F6 Observability** — the mediator is a single node through which all communication flows; it provides excellent observability but becomes a bottleneck at scale. Compare [Choreography](choreography.md) which scales at the cost of observability.
- **F4 Answer quality** — the mediator can synthesize, reconcile conflicting agent outputs, and inject relevant context, improving the quality of multi-agent collaboration.
- **F11 Operational complexity** — the mediator itself must be robust; its failure halts all coordination.

## Solution
A **mediator agent** (or mediator LLM) receives all messages from participants, maintains a shared conversation context, routes messages to the appropriate agents, synthesizes their responses, and resolves conflicts. Agents only know about the mediator, not each other.

<!-- TODO: replace with img/mediator.png once diagram is generated -->
```
Agent A ──► Mediator ◄── Agent B
Agent C ──►    │    ◄── Agent D
               │
           routes, contextualizes,
           resolves conflicts
               │
          ┌────┴────┐
          ▼         ▼
       Agent B   Agent C
```

## Sample Code
Runnable implementation: [samples/python/coordination/mediator.py](../../samples/python/coordination/mediator.py)

```python
mediator = MediatorAgent()
mediator.register("researcher", researcher_fn)
mediator.register("writer", writer_fn)
mediator.register("critic", critic_fn)

result = mediator.coordinate("write a research summary on quantum computing")
```

## Consequences
- ✅ N couplings instead of N² — adding a new agent is O(1) (F2 resolved)
- ✅ Centralized context management and conflict resolution (F4 improved)
- ✅ All communication visible through one node (F6 resolved)
- ❌ Mediator is a single point of failure (F11 introduced)
- ❌ Mediator becomes a bottleneck under high message volume (F9 cost)

## When to avoid
- When agents are truly independent and do not need to coordinate — direct calls are simpler.
- When you need maximum throughput with loose consistency — use [Choreography](choreography.md).
- When agent count is ≤ 3 — [Group Chat](group-chat.md) with a simple manager is sufficient.

## Failure Modes Mitigated
Per [FAILURE-MAP.md](../FAILURE-MAP.md):
- **FM-2.4 Information withholding** ◐ — the mediator distributes relevant context from each agent to others; information is not siloed in direct peer channels.
- **FM-2.5 Ignored other agent input** ◐ — the mediator synthesizes all agent inputs before routing; no single agent's output is silently ignored.
- **FM-2.2 Fail to ask clarification** ◐ — the mediator can identify when agents have contradictory outputs and request clarification from the relevant specialist.

## Known Uses
- **Sarkar & Sarkar (2025)** (arXiv:2506.05364) — maps the Mediator pattern to the "supervisor LLM" that routes between specialized agents in MCP-based systems.
- **AutoGen** — the `GroupChatManager` is a mediator that routes messages between agents in a group chat.
- **Microsoft Semantic Kernel** — the Planner as mediator, routing between skills/plugins.
- **OpenAI Swarm** — the "triage agent" that routes between specialized agents acts as a lightweight mediator.

## Related Patterns
- *alternative-to* [Peer-to-Peer Delegation](peer-to-peer-delegation.md) — mediator centralizes; P2P decentralizes.
- *alternative-to* [Choreography](choreography.md) — mediator provides control; choreography provides scale.
- *refines* [Group Chat](group-chat.md) — Mediator is a Group Chat where the manager has routing intelligence and context synthesis.
- *uses* [Agent Card Registry](../discovery/agent-card-registry.md) — to discover and address the agents it mediates.

## References
- Sarkar, A. & Sarkar, S. (2025). *Survey of LLM Agent Communication with MCP.* arXiv:2506.05364.
- Gamma, E. et al. (1994). *Design Patterns* — Mediator.
- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv:2503.13657.
