# Failure Map

*Which pattern do I reach for when I see this failure?*

This is the catalog's most distinctive artifact. It maps the **14 empirically-observed failure modes** of the Multi-Agent System Failure Taxonomy (MAST; Cemri et al., NeurIPS 2025, arXiv:2503.13657) to the patterns that mitigate them.

MAST analyzed **1,600+ execution traces across 7 multi-agent frameworks** and found **41–86.7% failure rates**. Its central finding bears repeating:

> Failures stem from **system-design issues**, not just model limitations. Better base models will *not* close the full taxonomy — these are architecture problems.

That is the entire thesis of this catalog: integration patterns are how you engineer reliability that scaling the model cannot buy. This map is how you navigate from a *symptom you observed* to a *pattern that addresses it*.

> **How to read this:** A ✅ means the pattern directly addresses that failure mode. A ◐ means it helps partially or as a secondary effect. Mitigation is not elimination — patterns reduce the probability and blast radius of a failure; they do not guarantee its absence.

---

## The 14 MAST failure modes

### Category 1 — Specification & System Design (FM-1.x)

| Mode | Failure | Mitigated by |
|------|---------|--------------|
| FM-1.1 | Disobey task specification | Orchestrator ◐, LLM-as-Judge ✅, Ensemble Judge ✅ |
| FM-1.2 | Disobey role specification | Content-Based Router ✅, Supervised Delegation ◐ |
| FM-1.3 | Step repetition | Checkpoint & Resume ✅, Idempotent Agent ✅, Orchestrator ◐ |
| FM-1.4 | Loss of conversation history / context | Blackboard ✅, Context Injection ✅, Checkpoint & Resume ✅ |
| FM-1.5 | Unaware of termination conditions | Orchestrator ✅, LLM-as-Judge ◐ |

### Category 2 — Inter-Agent Misalignment (FM-2.x)

| Mode | Failure | Mitigated by |
|------|---------|--------------|
| FM-2.1 | Conversation reset | Checkpoint & Resume ✅, Blackboard ◐ |
| FM-2.2 | Fail to ask for clarification | Dead Letter Agent ◐, Supervised Delegation ◐ |
| FM-2.3 | Task derailment | Orchestrator ✅, Content-Based Router ✅, Trust Boundary ◐ |
| FM-2.4 | Information withholding | Blackboard ✅, Broadcast Message ✅ |
| FM-2.5 | Ignored other agent's input | Mediator Agent ✅, Group Chat ✅, Orchestrator ◐ |
| FM-2.6 | Reasoning–action mismatch | LLM-as-Judge ✅, Reflection Loop ✅ |

### Category 3 — Task Verification & Termination (FM-3.x)

| Mode | Failure | Mitigated by |
|------|---------|--------------|
| FM-3.1 | Premature termination | Orchestrator ✅, Ensemble Judge ✅ |
| FM-3.2 | No or incomplete verification | LLM-as-Judge ✅, Ensemble Judge ✅, Dead Letter Agent ◐ |
| FM-3.3 | Incorrect verification | Ensemble Judge ✅, Trust Boundary ◐ |

---

## Inverse view — what each pattern defends against

The same data, indexed by pattern. Useful when evaluating whether a pattern earns its place in your architecture.

| Pattern | Primary failure modes addressed |
|---------|-------------------------------|
| **Orchestrator** | FM-1.5 (termination conditions), FM-3.1 (premature termination), FM-2.3 (derailment), FM-1.3 (step repetition) |
| **Trust Boundary** | FM-2.3 (derailment via injection), FM-3.3 (incorrect verification by compromised agent); plus AiTM/impersonation threats from the security literature |
| **Ensemble Judge** | FM-3.2 (incomplete verification), FM-3.3 (incorrect verification), FM-3.1 (premature termination), FM-1.1 (disobey task spec) |
| **LLM-as-Judge** | FM-3.2, FM-2.6, FM-1.1 |
| **Checkpoint & Resume** | FM-2.1 (conversation reset), FM-1.3, FM-1.4 |
| **Blackboard** | FM-1.4 (context loss), FM-2.4 (information withholding) |
| **Content-Based Router** | FM-1.2 (role disobedience), FM-2.3 (derailment) |
| **Group Chat** | FM-3.2 (incomplete verification, via maker-checker), FM-2.5 (ignored input), FM-2.6 (reasoning–action mismatch) |
| **Magentic** | FM-1.3 (step repetition, via ledger), FM-1.5 (termination, via stall detection) — note: also *introduces* derailment/termination risk |

---

## Security failures beyond MAST

MAST focuses on *capability/coordination* failures. The **security** patterns address a distinct failure class documented elsewhere in the literature — adversarial rather than accidental:

- **Agent-in-the-Middle (AiTM)** attacks → *Trust Boundary*, *Agent Proxy*
- **Prompt injection via external content** → *Prompt Firewall* (cf. Prompt Infection, arXiv:2410.07283)
- **Privilege escalation / over-broad tools** → *Least-Privilege Tool Scope*
- **Protocol confusion / downgrade (A2A+MCP)** → *Trust Boundary* (cf. arXiv:2505.03864)

Exception-handling failures are addressed by the *Exception Handler Chain* pattern, grounded in SHIELDA (arXiv:2508.07935), which shows that unstructured error handling is itself a major source of agentic-workflow failure.

---

## Caveats

- **Mitigation ≠ elimination.** Patterns lower probability and contain blast radius. A system using every pattern can still fail.
- **Patterns interact.** Applying *Ensemble Judge* without *Dead Letter Agent* leaves rejected outputs nowhere to go. Read the **Related Patterns** section of each.
- **The map evolves with the taxonomy.** MAST is empirical and will be revised; so will this map. Contributions that add known-use evidence for a mitigation are especially welcome.

---

## References

- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv:2503.13657. (NeurIPS 2025 Datasets & Benchmarks.)
- *SHIELDA: Structured Handling of Exceptions in LLM-Driven Agentic Workflows.* arXiv:2508.07935.
- Lee, D. & Tiwari, M. (2024). *Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems.* arXiv:2410.07283.
- *From Glue-Code to Protocols: A Critical Analysis of A2A and MCP Security.* arXiv:2505.03864.
