# Broker
**Category:** Discovery
**Maturity:** ★ Emerging
**Also known as:** Dynamic Dispatcher, Capability Broker, Service Broker, MCP Broker

## Intent
Dynamically match tasks to capability providers at runtime by negotiating availability, quality signals, and load — going beyond a static registry lookup to active selection and routing.

## Context
You have a pool of agents or tool providers, each with declared capabilities. Tasks arrive with capability requirements. An [Agent Card Registry](agent-card-registry.md) can list candidates by capability, but it cannot dynamically select the best match given load, quality history, cost, or version constraints.

## Problem
A static registry lookup returns all agents with a matching capability but does not answer: *which one should I call right now?* When multiple providers exist, the caller must implement selection logic (load balancing, quality-based routing, version preference, cost optimization). This selection logic gets duplicated across every caller, or left to ad-hoc choices that produce inconsistent results.

## Forces
- **F2 Coupling** — the broker decouples callers from specific provider instances; callers express *what* they need, the broker decides *who* delivers it.
- **F4 Answer quality** — quality-aware routing (prefer high-scoring providers, exclude degraded ones) improves average answer quality at the cost of broker complexity.
- **F9 Scalability** — the broker can distribute load across providers, enabling horizontal scale.
- **F11 Operational complexity** — the broker itself is non-trivial infrastructure: it needs health signals, quality scores, and load information from each provider. A buggy broker is worse than no broker (a single point of misrouting).
- **F1 Latency** — broker negotiation adds a selection step before the provider call. This is usually fast (in-memory scoring) but adds overhead.

## Solution
A **broker** maintains a registry of providers with their capabilities, health status, and quality scores. When a task arrives, the broker:
1. Filters providers by declared capability match.
2. Ranks candidates by quality score, load, and constraints.
3. Selects and forwards the task to the best candidate.
4. Records the outcome to update quality scores (optional feedback loop).

<!-- TODO: replace with img/broker.png once diagram is generated -->
```
Caller ──► Broker
              │
              ├─ filter by capability
              ├─ rank by quality/load
              ├─ select best provider
              │
              └──► Provider A  (best match)
                   Provider B  (available)
                   Provider C  (degraded — excluded)
```

## Sample Code
Runnable implementation: [samples/python/discovery/broker.py](../../samples/python/discovery/broker.py)

```python
broker = Broker()
broker.register("summarize", fast_summarizer, quality=0.9)
broker.register("summarize", accurate_summarizer, quality=0.95)

result = broker.dispatch("summarize", document)
# broker selects accurate_summarizer (higher quality score)
```

## Consequences
- ✅ Callers express capability needs; broker handles provider selection (F2 resolved)
- ✅ Load balancing and quality-aware routing without caller changes (F9 resolved)
- ✅ Degraded providers are excluded without caller awareness
- ❌ Broker is a single point of failure and a potential bottleneck (F11, F9 risk)
- ❌ Quality scores require feedback from outcomes — adds instrumentation overhead
- ❌ Selection policy must be designed; wrong policy causes systematic misrouting

## When to avoid
- When there is only one provider per capability — use [Agent Card Registry](agent-card-registry.md) directly.
- When callers can reasonably select providers themselves — avoid broker overhead.
- When the broker becomes the bottleneck for high-throughput tasks — consider decentralized routing.

## Failure Modes Mitigated
Per [FAILURE-MAP.md](../FAILURE-MAP.md):
- **FM-1.2 Disobey role specification** ◐ — the broker routes to providers with the declared capability, preventing tasks from reaching agents outside their role.
- **FM-2.3 Task derailment** ◐ — capability-matched routing reduces the chance a task reaches an incompatible provider that would mishandle it.

## Known Uses
- **MCP broker pattern** — the MCP specification describes broker-like selection of tool providers when multiple servers offer overlapping capabilities.
- **LangChain tool selection** — the agent/LLM selects among multiple registered tools based on capability descriptions (an LLM-driven broker).
- **Buschmann POSA1 Broker** — the classical object-oriented Broker pattern for distributed components; the agent catalog adapts it to capability-based LLM agent routing.
- **AWS API Gateway + Lambda** — a canonical infrastructure-level broker: routes requests to function providers by path and capability.

## Related Patterns
- *refines* [Agent Card Registry](agent-card-registry.md) — the Registry is a passive lookup; the Broker is an active selector.
- *uses* [Agent Card Registry](agent-card-registry.md) — the Broker uses the Registry as its candidate source.
- *complements* [Circuit Breaker](../resilience/circuit-breaker.md) — the Broker excludes providers that the Circuit Breaker has opened; the two patterns compose naturally.
- *alternative-to* [Content-Based Router](../routing/content-based-router.md) — CBR routes by task content; Broker routes by provider quality/load among capability-matched providers.

## References
- Buschmann, F. et al. (1996). *Pattern-Oriented Software Architecture* (POSA1) — Broker.
- Sarkar, A. & Sarkar, S. (2025). *Survey of LLM Agent Communication with MCP.* arXiv:2506.05364.
- Anthropic (2024). *Model Context Protocol specification.*
- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv:2503.13657.
