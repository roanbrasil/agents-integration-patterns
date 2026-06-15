"""
Circuit Breaker Pattern
CLOSED/OPEN/HALF_OPEN states protecting calls to a downstream agent.
"""
import time
from typing import Literal
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

State = Literal["CLOSED", "OPEN", "HALF_OPEN"]


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 2.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state: State = "CLOSED"
        self.opened_at: float = 0.0

    def call(self, fn, *args, **kwargs):
        if self.state == "OPEN":
            elapsed = time.time() - self.opened_at
            if elapsed >= self.recovery_timeout:
                print(f"[CircuitBreaker] Timeout elapsed ({elapsed:.1f}s). Transitioning to HALF_OPEN.")
                self.state = "HALF_OPEN"
            else:
                raise RuntimeError(f"[CircuitBreaker] Circuit is OPEN. Blocking call. ({elapsed:.1f}s elapsed)")

        try:
            result = fn(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        if self.state == "HALF_OPEN":
            print("[CircuitBreaker] Probe succeeded. Transitioning to CLOSED.")
        self.failure_count = 0
        self.state = "CLOSED"

    def _on_failure(self):
        self.failure_count += 1
        print(f"[CircuitBreaker] Failure #{self.failure_count} recorded.")
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.opened_at = time.time()
            print(f"[CircuitBreaker] Threshold reached. Transitioning to OPEN.")


call_count = 0


def flaky_downstream(prompt: str) -> str:
    global call_count
    call_count += 1
    if call_count <= 3:
        raise ConnectionError(f"Downstream unavailable (call #{call_count})")
    response = llm.invoke(prompt)
    return response.content if hasattr(response, "content") else str(response)


def main():
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=2.0)
    prompt = "In one sentence, what is a circuit breaker in software?"

    for attempt in range(1, 8):
        print(f"\n--- Attempt {attempt} | CB state: {cb.state} ---")
        try:
            result = cb.call(flaky_downstream, prompt)
            print(f"Success: {result}")
        except RuntimeError as e:
            print(f"Blocked: {e}")
        except ConnectionError as e:
            print(f"Downstream error: {e}")

        if attempt == 4:
            print(f"\n[main] Waiting {cb.recovery_timeout}s for circuit recovery timeout...")
            time.sleep(cb.recovery_timeout + 0.1)


if __name__ == "__main__":
    main()
