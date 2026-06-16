# Saga / Compensating Action
**Category:** Coordination
**Maturity:** ★ Emerging
**Also known as:** Compensating Transaction, Rollback Chain, Long-Running Transaction, Distributed Undo

## Intent
Execute a multi-step workflow where each step has a corresponding **compensating action**; if any step fails, run the compensations of all prior completed steps in reverse order to restore a consistent state.

## Context
You are building a multi-agent workflow that modifies external state across several steps — booking a flight, reserving inventory, charging a payment, sending a confirmation. The steps may involve different agents or external systems. A failure partway through leaves external state in an inconsistent, partially-applied state.

## Problem
A long-running multi-agent workflow cannot use database transactions (steps span multiple systems, agents, and time boundaries). When step N fails after steps 1…N-1 have already modified external state, the system is left in an inconsistent, partially-applied state. Without explicit rollback logic, human intervention is required to clean up after every failure.

## Forces
- **F4 Reliability** — the pattern's core benefit: partial failures are recoverable; the system can always reach a consistent state (either fully applied, or fully compensated).
- **F8 Determinism** — each step has an explicit forward action and an explicit compensation; the rollback path is as deterministic as the forward path.
- **F11 Operational complexity** — every step requires a compensation, doubling the code. Compensations must be idempotent (see [Idempotent Agent](../resilience/idempotent-agent.md)) and may not perfectly undo the original action (e.g., a sent email cannot be unsent — use a notification instead).
- **F3 Token cost** — compensation steps may require LLM calls (to generate cancellation messages, determine which records to roll back, etc.).

## Solution
Define each workflow step as a pair: a **forward action** and a **compensating action**. Execute steps in sequence, recording completed steps. On failure at step N, execute compensations for steps N-1, N-2, …, 1 in reverse order. Compensations must be idempotent and must be designed to work even if the forward action partially succeeded.

<!-- TODO: replace with img/saga.png once diagram is generated -->
```
Forward:   Step1 → Step2 → Step3 → [FAIL at Step4]
                                        │
Compensate:                        undo Step3
                                   undo Step2
                                   undo Step1
```

## Sample Code
Runnable implementation: [samples/python/coordination/saga.py](../../samples/python/coordination/saga.py)

```python
saga = Saga()
saga.step("reserve_inventory", reserve_fn, compensate=release_fn)
saga.step("charge_payment", charge_fn, compensate=refund_fn)
saga.step("send_confirmation", send_fn, compensate=send_cancellation_fn)

result = saga.execute(order)
# On failure at any step, prior compensations run automatically
```

## Consequences
- ✅ Partial failures produce a consistent (compensated) state — no orphaned external records (F4 resolved)
- ✅ Rollback path is explicit, auditable, and testable (F8 resolved)
- ❌ Every step requires a compensation, doubling the code (F11 introduced)
- ❌ Compensations may be imperfect (sent emails, published events cannot be truly undone)
- ❌ Compensation execution can itself fail — requires its own retry / dead letter handling

## When to avoid
- When steps do not modify external state (pure read / computation) — no compensation needed.
- When a workflow failure is acceptable to resolve manually — saga adds complexity only justified when automatic rollback is required.
- When true database transactions are available — use them instead.

## Failure Modes Mitigated
Per [FAILURE-MAP.md](../FAILURE-MAP.md):
- **FM-3.1 Premature termination** ✅ — a saga failure triggers compensations rather than abandoning the workflow in an inconsistent state; "terminated" is always in a consistent state.
- **FM-2.1 Conversation reset** ◐ — the compensation chain brings the system back to the pre-saga state, equivalent to resetting all side effects.

## Known Uses
- **EIP Saga** — Hohpe & Woolf's canonical pattern for long-running transactions.
- **Temporal Workflows** — saga with compensation activities is a first-class Temporal primitive; used extensively in financial and order management systems.
- **Microsoft Azure Durable Functions** — the Saga / Compensating Transaction pattern is one of the documented serverless workflow patterns.
- **Agent-based order management** — booking + inventory + payment + notification workflows are the canonical multi-agent saga use case.

## Related Patterns
- *uses* [Idempotent Agent](../resilience/idempotent-agent.md) — compensation steps must be idempotent; repeated compensation must not double-undo.
- *uses* [Checkpoint & Resume](../resilience/checkpoint-resume.md) — the saga step log is the natural checkpoint; resume can re-enter the compensation path.
- *used-by* [Dead Letter Agent](../resilience/dead-letter-agent.md) — if compensation itself fails, the failed compensation routes to the dead letter handler.
- *alternative-to* [Pipeline](../routing/pipeline.md) — a pipeline with no rollback vs. a saga with explicit compensation.

## References
- Hohpe, G. & Woolf, B. (2003). *Enterprise Integration Patterns* — Saga / Process Manager.
- Garcia-Molina, H. & Salem, K. (1987). *Sagas.* ACM SIGMOD.
- Microsoft (2024). *Azure Architecture Patterns — Saga.*
- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv:2503.13657.
