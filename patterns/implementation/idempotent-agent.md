# Idempotent Agent
**Category:** Implementation
**Maturity:** ★ Emerging
**Also known as:** At-Most-Once Execution, Deduplication Guard, Operation Idempotency

## Intent
Ensure that every agent action can be retried without causing duplicate side effects, by keying each operation on a stable identifier and skipping already-completed steps.

## Context
You have a multi-step agentic workflow where individual steps may fail and be retried — due to rate limits, transient errors, infrastructure restarts, or [Checkpoint & Resume](../resilience/checkpoint-resume.md) re-execution. Some steps have side effects: writing to a database, sending a message, calling an external API, charging a payment.

## Problem
When an agent retries a failed step, it cannot always tell whether the previous attempt succeeded before the connection dropped. Re-executing a non-idempotent action (create order, send email, charge card) causes duplicates. Without idempotency, retries are unsafe, so either developers avoid retries (risking incomplete workflows) or they accept duplicates (corrupting data).

## Forces
- **F4 Reliability vs. F8 Determinism** — reliable systems must retry on failure; deterministic systems must produce the same observable effect regardless of how many times a step runs. These two are in direct tension: idempotency is the mechanism that reconciles them.
- **F11 Operational complexity** — maintaining an idempotency store (a durable log of completed operations) adds infrastructure. An in-memory dict works for a single session; persistent storage (Redis, database) is required across restarts.
- **F3 Token cost** — idempotent LLM calls are rarely possible (LLM responses are non-deterministic); the pattern targets *tool calls and side-effecting actions*, not the LLM inference step itself.

## Solution
Assign a stable **idempotency key** to each operation (typically a hash of the step name + workflow run ID + input hash). Before executing, check whether the key already exists in the idempotency store; if it does, return the cached result and skip the action. If it does not, execute, record the key + result, and return.

<!-- TODO: replace with img/idempotent-agent.png once diagram is generated -->
```
Caller
  │  execute(step, inputs)
  ▼
IdempotencyGuard
  │ key = hash(run_id + step + inputs)
  ├─[key EXISTS]──► return stored_result   (no side effect)
  └─[key MISSING]─► Action ──► store(key, result) ──► return result
```

## Sample Code
Runnable implementation: [samples/python/implementation/idempotent_agent.py](../../samples/python/implementation/idempotent_agent.py)

```python
guard = IdempotencyGuard()

@guard.protect
def send_email(recipient: str, body: str) -> str:
    # executes at most once per (recipient, body) combination
    ...
```

## Consequences
- ✅ Retries are safe — no duplicate side effects (F4 and F8 reconciled)
- ✅ Compatible with [Checkpoint & Resume](../resilience/checkpoint-resume.md) — resume re-runs steps idempotently
- ❌ Requires a durable idempotency store for cross-restart safety (F11 introduced)
- ❌ Does not help with LLM inference steps — only with side-effecting tool calls
- ❌ Idempotency keys must be carefully designed; wrong keys cause either missed dedup or incorrect cache hits

## When to avoid
- When the workflow has no side-effecting steps (pure computation / read-only).
- When each run is designed to produce fresh results regardless (e.g., polling agents).

## Failure Modes Mitigated
Per [FAILURE-MAP.md](../FAILURE-MAP.md):
- **FM-1.3 Step repetition** ✅ — completed steps are recorded; re-execution returns the cached result without repeating the action.
- **FM-2.1 Conversation reset** ◐ — when combined with Checkpoint & Resume, idempotency ensures that resuming from a checkpoint does not re-trigger already-executed side effects.

## Known Uses
- **LangGraph** — checkpointed graphs re-enter from the last node; idempotent tool calls prevent duplicate API calls on resume.
- **12-Factor Agents** — "own your control flow" explicitly calls out idempotency as a first-class concern for agentic workflows.
- **Temporal Workflows** — activity idempotency is a core primitive; any workflow engine with replay semantics requires it.
- **Stripe API** — idempotency keys on payment endpoints are the canonical industry example; the same pattern applies to agent tool calls.

## Related Patterns
- *complements* [Checkpoint & Resume](../resilience/checkpoint-resume.md) — Checkpoint persists step state; Idempotent Agent makes re-execution of those steps safe.
- *used-by* [Saga / Compensating Action](../coordination/saga.md) — saga steps must be idempotent so that compensation can safely run after a partial failure.
- *complements* [Dead Letter Agent](../resilience/dead-letter-agent.md) — tasks that exhaust retries (even idempotent ones) route to the dead letter handler.

## References
- HumanLayer (2025). *12-Factor Agents* — "own your control flow." https://github.com/humanlayer/12-factor-agents
- Kleppmann, M. (2017). *Designing Data-Intensive Applications* — idempotency in distributed systems.
- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv:2503.13657.
