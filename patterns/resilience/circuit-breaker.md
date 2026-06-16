# Circuit Breaker
**Category:** Resilience
**Maturity:** ★★ Established
**Also known as:** Fault Isolator, Failure Detector, Upstream Protector

> Stop making calls to a failing agent or tool, allow time to recover, and automatically resume when healthy.

**EIP Analog:** No direct EIP analog — pattern originates in Michael Nygard's *Release It!* (2007)

---

## Intent

Wrap calls to external agents or tools in a stateful breaker that stops sending requests to a failing dependency, giving it time to recover, and automatically resumes when it is healthy.

---

## Context

Agent systems depend on external agents, tools, and APIs that can fail or degrade.

---

## Problem

When an agent or tool dependency fails repeatedly, continued retries amplify the load on the failing component, consume caller resources, and cascade failures to unrelated parts of the system. You need a way to detect sustained failures and stop hitting a broken dependency — while letting it recover.

---

## Forces

- **F4 Reliability** — prevents cascade failures by stopping calls to a failing downstream agent.
- **F1 Latency** — when OPEN, calls fail fast (no timeout wait), actually improving latency under failure conditions.
- **F6 Observability** — circuit state (CLOSED/OPEN/HALF_OPEN) is an explicit health signal.
- **F10 Adaptability** — the HALF_OPEN state enables automatic recovery when the downstream agent becomes healthy again.

---

## Solution

Wrap calls to external agents/tools in a circuit breaker with three states. **Closed (normal):** calls pass through; failures are counted. **Open (tripped):** after N consecutive failures, the circuit opens; all calls fail immediately without reaching the downstream agent. **Half-Open (probing):** after a timeout, one probe call is allowed; if it succeeds, the circuit closes; if it fails, it reopens.

---

## Diagram

![Circuit Breaker — Agent A call passes through Circuit Breaker with three states: CLOSED passes to Agent B (healthy), OPEN returns Error (fast), HALF probe tests Agent B (testing)](../../img/circuit-break.png)

---

## Participants

| Participant | Role |
|---|---|
| **Caller Agent** | Makes calls through the circuit breaker |
| **Circuit Breaker** | Tracks failure state; decides whether to pass, block, or probe |
| **Downstream Agent / Tool** | The dependency being protected; gets recovery time when circuit is open |

---

## Sample Code

Runnable implementation: [samples/python/resilience/circuit_breaker.py](../../samples/python/resilience/circuit_breaker.py)

```python
# Circuit breaker for agent/tool calls
import asyncio
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=30):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.opened_at: datetime | None = None

    async def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if datetime.now() - self.opened_at > timedelta(seconds=self.recovery_timeout):
                self.state = CircuitState.HALF_OPEN
            else:
                raise RuntimeError("Circuit is OPEN — downstream agent unavailable")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = datetime.now()


# Usage with an A2A agent call
breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)

async def call_research_agent(query: str) -> str:
    return await breaker.call(a2a_client.send_task_and_wait, query)
```

---

## Consequences

- ✅ Prevents cascade failures (F4 resolved)
- ✅ Fast failure when OPEN — better than timeout (F1 resolved)
- ✅ Explicit health state observable (F6 resolved)
- ✅ Automatic recovery via HALF_OPEN (F10 resolved)
- ❌ Threshold tuning required — too sensitive trips on transient errors; too lax lets failures cascade

---

## When to avoid

- When the downstream agent is highly reliable and failure is rare — the breaker adds overhead without value.
- When callers cannot handle fast failure and need a blocking wait — circuit breaker requires callers to handle the OPEN state.

---

## Failure Modes Mitigated

Per [FAILURE-MAP.md](../FAILURE-MAP.md):
- **FM-3.1 Premature termination** ◐ — by isolating failing agents, the circuit breaker prevents one agent's failure from terminating the entire workflow.

---

## Known Uses

- **Spring AI Resilience4j integration** — Spring AI supports Resilience4j circuit breakers wrapping tool and agent calls
- **LangChain retry policies** — `RetryWithError` and custom retry handlers implement failure counting analogous to circuit breaker logic
- **Temporal workflow activities** — Temporal's retry policy and heartbeat timeout implement circuit-breaker-like behavior for long-running agent activities

---

## Related Patterns

- *complements* [Dead Letter Agent](dead-letter-agent.md) — circuit breaker prevents new calls; dead letter handles the ones that got through and failed.
- *complements* [Agent Proxy](../discovery/agent-proxy.md) — the proxy is where the circuit breaker is typically implemented.
- *used-by* [Magentic Orchestration](../coordination/magentic.md) — stall detection in Magentic is a soft circuit breaker for emergent plans.

---

## References

- Nygard, M. (2007). *Release It!* — Circuit Breaker pattern.
- Cemri, M. et al. (2025). arXiv:2503.13657.
- [Resilience4j Circuit Breaker](https://resilience4j.readme.io/docs/circuitbreaker)
- [Spring AI: Resilience Patterns](https://docs.spring.io/spring-ai/reference/)
