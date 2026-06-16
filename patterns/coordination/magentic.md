# Magentic Orchestration

**Category:** Coordination
**Maturity:** ☆ Proposed
**Also known as:** Task-Ledger Orchestration, Dynamic Planner, Open-Ended Orchestration

## Intent

Solve open-ended problems that have no predetermined plan by having a manager agent build and continuously refine a **task ledger** in collaboration with specialized agents, adapting the plan as the context evolves.

## Context

You face a problem complex and open-ended enough that you cannot write the workflow graph in advance (unlike *Orchestrator*) and the right sequence of specialists is not knowable upfront (unlike a fixed pipeline). The approach itself must be discovered as part of solving the problem.

## Problem

A pre-defined plan (Orchestrator) cannot express a workflow whose very structure is unknown until work begins. Pure event-driven coordination (Choreography) gives no global view to reason about progress. You need something that *plans as it goes* while still maintaining a coherent, inspectable record of what has been done and what remains.

## Forces

- **F10 Adaptability vs. F8 Determinism** — maximal adaptability to unforeseen problem structure, at the cost of reproducibility: two runs may take different paths.
- **F6 Observability vs. F10** — the task ledger restores some observability (you can read the evolving plan), but the plan is no longer fixed, so you cannot fully predict execution.
- **F4 Reliability vs. F11 Operational complexity** — capable of handling problems nothing simpler can, but the most complex and failure-prone pattern in the catalog.

Magentic sits at the far adaptability end of the coordination spectrum: Orchestrator (fixed plan) → Supervised Delegation (monitored plan) → **Magentic (emergent plan)** → Choreography (no plan).

## Solution

A **manager agent** maintains a *task ledger* — a living document of facts gathered, the current plan, completed steps, and open questions. It assigns tasks to specialized agents (which typically have state-changing tools), incorporates their results, and **re-plans**: updating the ledger, reordering or adding steps, and detecting when it is stuck. Progress is tracked against the ledger rather than against a fixed graph. An iteration/stall limit prevents unbounded looping.

![Magentic](../../img/magentic.svg)

## Sample Code

Runnable, tested implementation: [`samples/coordination/magentic/`](../../samples/coordination/magentic/)

```python
# Excerpt — the manager maintains a ledger and re-plans each round
mgr = MagenticManager(planner=plan_fn, max_rounds=8, stall_limit=2)
mgr.register("researcher", researcher); mgr.register("writer", writer)
ledger = mgr.run(goal="produce a competitive analysis of X")
# ledger.plan evolved across rounds; ledger.done lists completed steps
```

## Consequences

- ✅ Handles open-ended goals with no upfront plan — the only pattern that does (resolves F10).
- ✅ The task ledger keeps an emergent process inspectable (partially resolves F6).
- ❌ Non-deterministic: different runs may diverge; hard to test and reproduce (introduces F8 cost).
- ❌ Highest operational complexity and failure surface in the catalog (introduces F11); demands strict stall/iteration limits.

## When to avoid

- The workflow *can* be specified in advance — use **Orchestrator** and get determinism for free.
- You need reproducible, auditable runs (regulated domains): an emergent plan is hard to certify.
- The problem decomposes into a known set of specialists — use **Handoff/Routing** or **Supervised Delegation**.

## Failure Modes Mitigated

Per [FAILURE-MAP.md](../FAILURE-MAP.md):

- **FM-1.3 Step repetition** ◐ — the ledger records completed steps, reducing redundant work.
- **FM-1.5 Unaware of termination conditions** ◐ — stall detection and the ledger's open-questions list give explicit stop signals.

⚠️ Note: Magentic also *introduces* exposure to several MAST modes (derailment, premature termination) precisely because the plan is emergent. It is a power tool, not a safe default — its own failure surface is why it is rated ☆ Proposed.

## Known Uses

- **Microsoft Magentic-One / Agent Framework** — magentic orchestration with a task-ledger manager (Azure Architecture Center, 2026).

## Related Patterns

- *alternative-to* **[Orchestrator](orchestrator.md)** — fixed plan; choose it whenever the plan is knowable.
- *alternative-to* **[Supervised Delegation](supervised-delegation.md)** — monitored but pre-decomposed; Magentic re-decomposes at runtime.
- *uses* **[Checkpoint & Resume](../resilience/checkpoint-resume.md)** — the task ledger is a natural checkpoint boundary for long, expensive runs.
- *uses* **[Dead Letter Agent](../resilience/dead-letter-agent.md)** — escalation target when the stall limit is reached.

## References

- Microsoft (2026). *AI Agent Orchestration Patterns* — Magentic. Azure Architecture Center.
- Fourney, A. et al. (2024). *Magentic-One: A Generalist Multi-Agent System.* Microsoft Research.
- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv:2503.13657.
