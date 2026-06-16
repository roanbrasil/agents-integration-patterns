# Exception Handler Chain
**Category:** Resilience
**Maturity:** ★ Emerging
**Also known as:** Structured Exception Handling, Error Handler Chain, SHIELDA Handler, Fault Escalation Chain

## Intent
Give each category of agent failure its own structured handler — retry, fallback, human escalation — arranged as a chain of responsibility so that unhandled exceptions propagate to progressively higher-severity handlers.

## Context
You are building a multi-agent workflow where agents call LLMs, external tools, and other agents. Runtime failures are inevitable: rate limits, hallucinated tool arguments, timeout, context overflow, unexpected output formats. Currently these failures surface as unhandled exceptions that terminate the workflow.

## Problem
A single try/except block at the workflow level loses the structure needed to recover correctly: a transient rate-limit error warrants a brief retry; a malformed LLM output warrants a prompt correction; a repeated tool error warrants fallback to a simpler agent; a policy violation warrants immediate human escalation. Treating all exceptions the same (log + abort) wastes recovery opportunities and produces low-signal error reporting.

## Forces
- **F4 Reliability** — structured exception handling converts many "fatal" failures into recoverable events, dramatically improving end-to-end reliability.
- **F6 Observability** — each handler produces a typed, logged event (RetryEvent, FallbackEvent, EscalationEvent) rather than a raw stack trace, making failure analysis actionable.
- **F11 Operational complexity** — a chain of handlers is more code than a single catch. The complexity is justified when the workflow has multiple distinct failure modes that warrant different recovery actions.
- **F1 Latency** — retry and fallback handlers add latency; escalation handlers add human-loop latency. These are deliberate trade-offs for reliability.

## Solution
Define a chain of **ExceptionHandler** objects. Each handler declares which exception types it handles. When an agent action raises an exception, the chain is traversed in order; the first handler that matches executes its recovery logic. If no handler matches, the exception propagates (ultimately to the workflow's dead letter handler).

Canonical handler types (from SHIELDA, arXiv:2508.07935):
1. **RetryHandler** — transient errors (rate limits, timeouts): wait and retry up to N times.
2. **FallbackHandler** — repeated failures: delegate to a simpler / more reliable agent.
3. **CorrectHandler** — malformed outputs: re-invoke with a correction prompt.
4. **EscalateHandler** — policy violations, max retries exceeded: pause and request human input.

<!-- TODO: replace with img/exception-handler-chain.png once diagram is generated -->
```
Agent raises Exception
       │
       ▼
  RetryHandler ──[matches? retry≤N]──► retry action
       │ no match / exhausted
       ▼
  FallbackHandler ──[matches?]──► invoke fallback agent
       │ no match
       ▼
  EscalateHandler ──[always]──► notify human, pause workflow
```

## Sample Code
Runnable implementation: [samples/python/resilience/exception_handler_chain.py](../../samples/python/resilience/exception_handler_chain.py)

```python
chain = (
    ExceptionHandlerChain()
    .add(RetryHandler(on=RateLimitError, max_retries=3, delay=1.0))
    .add(FallbackHandler(on=OutputFormatError, fallback=simple_agent))
    .add(EscalateHandler(on=Exception, notify=human_notify))
)
result = chain.execute(agent_action, inputs)
```

## Consequences
- ✅ Each failure mode has a targeted, recoverable response (F4 resolved)
- ✅ Typed handler events are loggable and analyzable (F6 resolved)
- ✅ Human escalation is explicit and auditable, not silent data loss
- ❌ More code than a single catch block (F11 introduced)
- ❌ Handler ordering matters; wrong order can shadow exceptions

## When to avoid
- When the workflow is short-lived and all failures should abort — a single catch + dead letter is simpler.
- When exception categories are not yet known — define a single escalate handler first and refine as failure patterns emerge.

## Failure Modes Mitigated
Per [FAILURE-MAP.md](../FAILURE-MAP.md):
- **FM-3.1 Premature termination** ✅ — retry and fallback handlers recover from transient failures that would otherwise terminate the workflow.
- **FM-3.2 No or incomplete verification** ◐ — the correct handler verifies output format and re-invokes with a correction prompt, acting as a lightweight output verifier.
- **FM-1.5 Unaware of termination conditions** ◐ — escalation handlers make termination explicit (human decides) rather than silent (exception propagates unhandled).

## Known Uses
- **SHIELDA** (arXiv:2508.07935) — proposes structured exception handling for LLM-driven agentic workflows; identifies retry, fallback, correct, and escalate as the canonical handler types.
- **LangChain** — fallback chains (`RunnableWithFallbacks`) implement the fallback handler type.
- **AutoGen** — nested conversation retry and human-in-the-loop escalation implement the retry and escalate handler types.
- **CrewAI** — task error handling with max retries and fallback agents.

## Related Patterns
- *complements* [Dead Letter Agent](dead-letter-agent.md) — EscalateHandler routes to a human or dead letter when the chain is exhausted.
- *complements* [Circuit Breaker](circuit-breaker.md) — circuit breaker prevents calls to a failing agent; EHC handles failures that get through.
- *used-by* [Magentic Orchestration](../coordination/magentic.md) — stall detection is a lightweight EHC (escalate after stall_limit consecutive non-progress rounds).

## References
- *SHIELDA: Structured Handling of Exceptions in LLM-Driven Agentic Workflows.* arXiv:2508.07935.
- Gamma, E. et al. (1994). *Design Patterns* — Chain of Responsibility.
- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv:2503.13657.
