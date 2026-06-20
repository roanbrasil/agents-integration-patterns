# Forces

*The recurring tensions that every integration pattern must balance.*

A **force** is a consideration that pulls a design decision in a particular direction. Patterns are interesting precisely because forces *conflict* — resolving one aggravates another. Naming forces explicitly is what makes a catalog **generative**: it lets a reader reason about *why* to reach for a pattern, not just *how* to apply it (Alexander et al. 1977; Gamma et al. 1994).

Every pattern in this catalog references these shared forces in its **Forces** section. Think of this file as the catalog's shared vocabulary of trade-offs.

---

## The force catalog

| ID | Force | Pulls toward | Pulls away from |
|----|-------|--------------|-----------------|
| **F1** | **Latency** | Direct calls, fewer hops, local execution | Intermediaries, validation layers, ensembles |
| **F2** | **Coupling** | Decoupling via brokers, events, proxies | Direct point-to-point addressing |
| **F3** | **Token cost** | Single agent, one pass, terse context | Ensembles, debate, large injected context |
| **F4** | **Answer quality / reliability** | Multiple perspectives, verification, retries | Single-shot, unverified output |
| **F5** | **Blast radius** | Least privilege, scoped tools, trust tiers | Broad capabilities, shared credentials |
| **F6** | **Observability / debuggability** | Centralized orchestration, explicit state | Emergent choreography, implicit flow |
| **F7** | **Trust asymmetry** | Authentication, sanitization, boundaries | Open delegation, unchecked external content |
| **F8** | **Determinism / reproducibility** | Fixed workflows, checkpoints, idempotency | Adaptive routing, autonomous delegation |
| **F9** | **Scalability** | Decentralization, parallelism, statelessness | Central coordinators, shared mutable state |
| **F10** | **Adaptability** | Dynamic routing, autonomous agents | Pre-defined plans, rigid pipelines |
| **F11** | **Operational complexity** | Fewer moving parts, simple topologies | Registries, brokers, message infrastructure |
| **F12** | **Completion specificity** | Precise, verifiable exit criteria | Flexible, judgment-based termination |
| **F13** | **Context pollution** | Clean context at each handoff, pruned history | Rich accumulated history, full trace |
| **F14** | **Transport latency / reliability** | Low-latency, multiplexed, reconnection-resilient transport | Simple TCP/HTTP with higher overhead per connection |

---

## How forces drive the catalog

A few illustrative tensions that recur across patterns:

- **F1 Latency vs. F4 Reliability.** *Ensemble Judge* and *Scatter-Gather* spend latency and tokens (F1, F3) to buy answer quality (F4). *Direct Message* does the opposite.
- **F6 Observability vs. F9 Scalability.** *Orchestrator* centralizes state for debuggability (F6) at the cost of becoming a bottleneck (F9). *Choreography* inverts this exactly.
- **F5 Blast radius vs. F10 Adaptability.** *Least-Privilege Tool Scope* and *Trust Boundary* shrink blast radius (F5) by constraining what agents can do — which limits autonomous adaptability (F10).
- **F8 Determinism vs. F10 Adaptability.** *Checkpoint & Resume* and *Idempotent Agent* buy reproducibility (F8); *Peer-to-Peer Delegation* trades it for runtime adaptability (F10).
- **F12 Completion specificity vs. F10 Adaptability.** *Reflection Loop* and *Orchestrator* enforce precise exit criteria (F12) which limits flexible judgment (F10); *Choreography* leaves termination implicit.
- **F13 Context pollution vs. F4 Answer quality.** *Reflection Loop* and *Checkpoint & Resume* require pruning accumulated critique history (F13 under control) to avoid degrading later iterations; keeping full history (F4) risks the model fixating on early errors.
- **F14 Transport latency vs. F8 Determinism.** HTTP/3 / QUIC (F14 optimized) introduces 0-RTT replay risk unless combined with server-side replay tokens — use with *Idempotent Agent* (F8) to stay safe. HTTP/2 is F14-good and replay-safe by default.

When two patterns are listed as *alternative-to* each other in their **Related Patterns** section, it is almost always because they resolve the **same forces in opposite directions**. The right choice depends on which force dominates in your context.

---

## References

- Alexander, C. et al. (1977). *A Pattern Language.*
- Gamma, E. et al. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software.*
- Hohpe, G. & Woolf, B. (2003). *Enterprise Integration Patterns.*
