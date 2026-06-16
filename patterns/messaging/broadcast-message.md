# Broadcast Message
**Category:** Messaging
**Maturity:** ★★ Established
**Also known as:** Publish-Subscribe, Fan-Out, Event Broadcast

## Intent
Send information from one agent to all interested agents simultaneously without knowing who they are.

## Context
An agent produces information — an observation, a state change, or a completed subtask result — that multiple downstream agents need to act upon, but the publisher does not know (and should not need to know) who they are.

## Problem
An agent produces information — a completed subtask result, an observation, a state change — that multiple downstream agents need to act upon. The producer should not need to know who the consumers are, and consumers should be able to join or leave without modifying the producer.

## Forces
- **F2 Coupling** — the pattern's primary benefit: the publisher is fully decoupled from subscribers; either side can change without modifying the other.
- **F9 Scalability** — subscribers can be added or removed without touching the publisher, enabling horizontal scale.
- **F1 Latency / F4 Reliability risk** — if subscribers produce new messages in reaction, feedback loops can cascade into message storms.

## Solution
Publish the message to a shared channel or topic. Interested agents subscribe to the channel and react independently. The publisher has no knowledge of subscribers — it only knows the topic it publishes to. A message broker or event bus routes copies to all active subscribers.

![Broadcast Message — Agent A (Publisher) publishes to Agent B, C, and D simultaneously](../../img/broadcast-message.png)

## Sample Code
Runnable implementation: [samples/python/messaging/broadcast_message.py](../../samples/python/messaging/broadcast_message.py)

## Consequences
- ✅ Decoupled — publisher unaware of subscribers (F2 resolved)
- ✅ Easily extensible — add agents without modifying publisher (F9 resolved)
- ❌ No delivery guarantee without infrastructure
- ❌ Risk of message storms if subscribers produce new messages (F1, F4 risk)

## When to avoid
- When you need delivery confirmation from each subscriber — use Direct Message with acknowledgment.
- When only one specific agent should act — use Direct Message.
- When subscriber reactions could create feedback loops without a circuit breaker.

## Failure Modes Mitigated
Per [FAILURE-MAP.md](../FAILURE-MAP.md):
- **FM-2.4 Information withholding** ✅ — all interested agents receive the same message simultaneously; no agent is excluded by design.
- **FM-2.5 Ignored other agent's input** ◐ — broadcast ensures all agents have the information, reducing selective ignorance.

## Known Uses
- **AutoGen GroupChat** — the GroupChatManager broadcasts each agent message to all participants in the group
- **CrewAI event-driven flows** — task completion events can trigger multiple downstream crew members
- **Kafka-backed agent pipelines** — agents publish results to Kafka topics; downstream specialist agents subscribe

## Related Patterns
- *alternative-to* [Direct Message](direct-message.md) — when multiple agents need the same information.
- *used-by* [Scatter-Gather](../routing/scatter-gather.md) — scatter uses broadcast semantics to fan out.
- *complements* [Blackboard](blackboard.md) — broadcast pushes; blackboard pulls.

## References
- Hohpe, G. & Woolf, B. (2003). *Enterprise Integration Patterns* — Publish-Subscribe Channel.
- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv:2503.13657.
