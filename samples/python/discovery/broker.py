"""Broker Pattern — dynamic capability-to-provider matching at runtime.

Goes beyond a static registry: ranks providers by quality score and load,
routes to the best match, and records outcomes to update scores.

Run: python3 discovery/broker.py
See: patterns/discovery/broker.md
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ProviderRecord:
    name: str
    capability: str
    fn: Callable[..., Any]
    quality: float = 1.0
    load: int = 0
    calls: int = 0
    errors: int = 0

    def score(self) -> float:
        load_penalty = self.load * 0.1
        return max(0.0, self.quality - load_penalty)


class Broker:
    """Dynamically matches tasks to capability providers."""

    def __init__(self) -> None:
        self._providers: list[ProviderRecord] = []

    def register(
        self, capability: str, fn: Callable, name: str = "", quality: float = 1.0
    ) -> "Broker":
        rec = ProviderRecord(
            name=name or fn.__name__,
            capability=capability,
            fn=fn,
            quality=quality,
        )
        self._providers.append(rec)
        return self

    def _candidates(self, capability: str) -> list[ProviderRecord]:
        return [p for p in self._providers if p.capability == capability and p.score() > 0]

    def dispatch(self, capability: str, *args: Any, **kwargs: Any) -> Any:
        candidates = self._candidates(capability)
        if not candidates:
            raise RuntimeError(f"no provider available for capability: {capability!r}")

        best = max(candidates, key=lambda p: p.score())
        best.load += 1
        best.calls += 1
        print(f"[broker] {capability!r} → {best.name!r} (score={best.score():.2f})")

        try:
            result = best.fn(*args, **kwargs)
            best.quality = min(1.0, best.quality + 0.01)
            return result
        except Exception:
            best.errors += 1
            best.quality = max(0.0, best.quality - 0.2)
            raise
        finally:
            best.load -= 1

    def status(self) -> list[dict]:
        return [
            {
                "name": p.name,
                "capability": p.capability,
                "score": round(p.score(), 3),
                "calls": p.calls,
                "errors": p.errors,
            }
            for p in self._providers
        ]


def main() -> None:
    print("=== Broker Pattern ===\n")

    def fast_summarizer(text: str) -> str:
        return f"[fast] summary: {text[:40]}..."

    def accurate_summarizer(text: str) -> str:
        return f"[accurate] detailed summary of '{text[:30]}...': key points extracted."

    def unstable_summarizer(text: str) -> str:
        if random.random() < 0.5:
            raise RuntimeError("transient error")
        return f"[unstable] summary: {text[:30]}"

    broker = (
        Broker()
        .register("summarize", fast_summarizer, name="fast", quality=0.7)
        .register("summarize", accurate_summarizer, name="accurate", quality=0.95)
        .register("summarize", unstable_summarizer, name="unstable", quality=0.6)
    )

    document = "The quick brown fox jumped over the lazy dog. " * 5

    print("--- 5 dispatch calls ---")
    for i in range(5):
        try:
            result = broker.dispatch("summarize", document)
            print(f"  call {i + 1}: {result[:60]}")
        except RuntimeError as e:
            print(f"  call {i + 1}: error — {e}")

    print("\n--- Provider status ---")
    for s in broker.status():
        print(f"  {s['name']:12} score={s['score']:.3f}  calls={s['calls']}  errors={s['errors']}")


if __name__ == "__main__":
    main()
