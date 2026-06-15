# Choreography

> Agents coordinate through events without a central controller — each agent knows what to do when it receives a specific event.

**Category:** coordination
**EIP Analog:** [Event-Driven Consumer](https://www.enterpriseintegrationpatterns.com/patterns/messaging/EventDrivenConsumer.html)

---

## Also Known As

Event-Driven Coordination, Reactive Agent Network, Decentralized Workflow

---

## Problem

Centralized orchestration creates bottlenecks and single points of failure. In high-scale or highly dynamic systems, you need agents to coordinate without depending on a coordinator being alive. Adding new agents should not require modifying a central workflow definition.

---

## Solution

Each agent subscribes to events relevant to its role and publishes events when it completes its work. No agent knows the global flow — each knows only its own triggers (input events) and outputs (published events). The workflow emerges from the interaction of locally-rational agents.

---

## Diagram

```
  [task_created]
       │
       ▼
  ┌─────────┐
  │ Agent A │ ──publishes──► [data_extracted]
  └─────────┘                       │
                                    ▼
                              ┌─────────┐
                              │ Agent B │ ──publishes──► [analyzed]
                              └─────────┘                    │
                                                             ▼
                                                       ┌─────────┐
                                                       │ Agent C │ ──► [done]
                                                       └─────────┘
```

---

## Participants

| Participant | Role |
|---|---|
| **Event Agents** | Each subscribes to trigger events, does its work, publishes result events |
| **Event Bus / Broker** | Routes events to all interested subscribers (Kafka, Redis, NATS) |
| **Event Schema** | The contract between agents — what each event contains |

---

## Consequences

**Benefits:**
- ✅ Highly decoupled — agents developed, deployed, and scaled independently
- ✅ No single point of failure in the coordination layer
- ✅ Easy to add new agents by subscribing to existing events

**Trade-offs:**
- ❌ Global workflow is implicit — understanding the full flow requires reading all agents
- ❌ Debugging failures requires distributed tracing across agents
- ❌ Compensating for partial failures (saga pattern) is complex without a coordinator

---

## Implementation

```python
# Choreography using Redis Streams as the event bus
import asyncio
import redis.asyncio as redis
import json

r_client = None  # shared Redis client

async def agent_a_extract(stream_in="tasks", stream_out="extracted"):
    """Agent A: subscribes to 'tasks', publishes to 'extracted'"""
    r = await redis.from_url("redis://localhost")
    last_id = "0"
    while True:
        events = await r.xread({stream_in: last_id}, block=1000, count=1)
        for _, messages in events:
            for msg_id, data in messages:
                result = {"text": f"extracted from: {data[b'input'].decode()}"}
                await r.xadd(stream_out, result)
                last_id = msg_id

async def agent_b_analyze(stream_in="extracted", stream_out="analyzed"):
    """Agent B: subscribes to 'extracted', publishes to 'analyzed'"""
    r = await redis.from_url("redis://localhost")
    last_id = "0"
    while True:
        events = await r.xread({stream_in: last_id}, block=1000, count=1)
        for _, messages in events:
            for msg_id, data in messages:
                result = {"analysis": f"analyzed: {data[b'text'].decode()}"}
                await r.xadd(stream_out, result)
                last_id = msg_id

# Run agents independently (each in its own process in production)
async def main():
    await asyncio.gather(agent_a_extract(), agent_b_analyze())
```

---

## Known Uses

- **Kafka-backed agentic pipelines** — each agent is a consumer group on one topic and a producer on another; no coordinator needed
- **CrewAI event-driven flows** — task completion events trigger subscribed crew members without a central manager
- **Microservices-style agent sagas** — agents implement compensating transactions by subscribing to failure events

---

## Related Patterns

- [Orchestrator](./orchestrator.md) — centralized alternative; use when the workflow is well-defined and observability is a priority
- [Broadcast Message](../messaging/broadcast-message.md) — the communication primitive that enables choreography
- [Dead Letter Agent](../resilience/dead-letter-agent.md) — catch unhandled events in choreography-based systems

---

## References

- Richardson, C. (2018). *Microservices Patterns*. Manning. Chapter 4: Managing transactions with sagas.
- arXiv:2501.06322 — characterizes peer-to-peer (choreography) vs. centralized (orchestration) as a primary structural dimension
