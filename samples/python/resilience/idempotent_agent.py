"""Idempotent Agent Pattern — at-most-once execution for side-effecting steps.

Assigns a stable idempotency key to each operation; skips re-execution if the
key was already recorded. Safe to combine with Checkpoint & Resume.

Run: python3 resilience/idempotent_agent.py
See: patterns/resilience/idempotent-agent.md
"""

from __future__ import annotations

import hashlib
import json
from functools import wraps
from typing import Any, Callable


class IdempotencyGuard:
    """Deduplicates side-effecting calls by key = hash(step + inputs)."""

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def _key(self, step: str, args: tuple, kwargs: dict) -> str:
        raw = json.dumps({"step": step, "args": list(args), "kwargs": kwargs}, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def execute(self, step: str, fn: Callable, *args: Any, **kwargs: Any) -> Any:
        key = self._key(step, args, kwargs)
        if key in self._store:
            print(f"[idempotent] SKIP  {step!r} (key={key})")
            return self._store[key]
        print(f"[idempotent] RUN   {step!r} (key={key})")
        result = fn(*args, **kwargs)
        self._store[key] = result
        return result

    def protect(self, fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return self.execute(fn.__name__, fn, *args, **kwargs)
        return wrapper

    @property
    def completed(self) -> set[str]:
        return set(self._store.keys())


def simulate_send_email(to: str, subject: str) -> str:
    return f"sent:{to}:{subject}"


def simulate_create_record(name: str, value: int) -> dict:
    return {"id": f"rec_{name}", "value": value, "status": "created"}


def main() -> None:
    print("=== Idempotent Agent Pattern ===\n")
    guard = IdempotencyGuard()

    # First execution — runs the action
    r1 = guard.execute("send_email", simulate_send_email, "alice@example.com", "Welcome")
    print(f"Result 1: {r1}\n")

    # Retry with same args — skips the action, returns cached result
    r2 = guard.execute("send_email", simulate_send_email, "alice@example.com", "Welcome")
    print(f"Result 2 (retry): {r2}\n")
    assert r1 == r2, "idempotent: same result on retry"

    # Different args → different key → runs again
    r3 = guard.execute("send_email", simulate_send_email, "bob@example.com", "Welcome")
    print(f"Result 3 (diff recipient): {r3}\n")

    @guard.protect
    def create_record(name: str, value: int) -> dict:
        return simulate_create_record(name, value)

    rec1 = create_record("order_42", 100)
    rec2 = create_record("order_42", 100)  # idempotent — skipped
    assert rec1 == rec2
    print(f"Record (idempotent): {rec1}")
    print(f"\nCompleted keys: {len(guard.completed)}")


if __name__ == "__main__":
    main()
