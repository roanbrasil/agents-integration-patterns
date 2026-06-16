"""Saga / Compensating Action Pattern — automatic rollback for multi-step workflows.

Each step has a forward action and a compensating action. On failure,
compensations run in reverse order for all completed steps.

Run: python3 coordination/saga.py
See: patterns/coordination/saga.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class SagaStep:
    name: str
    action: Callable[..., Any]
    compensate: Callable[..., Any]


@dataclass
class SagaResult:
    success: bool
    completed: list[str] = field(default_factory=list)
    compensated: list[str] = field(default_factory=list)
    failed_at: str = ""
    error: str = ""
    outputs: dict[str, Any] = field(default_factory=dict)


class Saga:
    """Execute steps forward; on failure, compensate in reverse."""

    def __init__(self) -> None:
        self._steps: list[SagaStep] = []

    def step(self, name: str, action: Callable, compensate: Callable) -> "Saga":
        self._steps.append(SagaStep(name=name, action=action, compensate=compensate))
        return self

    def execute(self, *args: Any, **kwargs: Any) -> SagaResult:
        result = SagaResult(success=False)
        completed: list[tuple[SagaStep, Any]] = []

        current_input = kwargs or (args[0] if args else {})
        for step in self._steps:
            try:
                print(f"[saga] ▶ {step.name}")
                output = step.action(current_input)
                result.outputs[step.name] = output
                result.completed.append(step.name)
                completed.append((step, current_input))
                if isinstance(output, dict):
                    current_input = {**current_input, **output}
            except Exception as exc:
                result.failed_at = step.name
                result.error = str(exc)
                print(f"[saga] ✗ {step.name} failed: {exc}")
                for done_step, done_input in reversed(completed):
                    try:
                        print(f"[saga] ↩ compensate {done_step.name}")
                        done_step.compensate(result.outputs.get(done_step.name, done_input))
                        result.compensated.append(done_step.name)
                    except Exception as comp_exc:
                        print(f"[saga] ✗ compensation failed for {done_step.name}: {comp_exc}")
                return result

        result.success = True
        return result


def main() -> None:
    print("=== Saga / Compensating Action Pattern ===\n")

    reserved: dict = {"items": []}
    charged: dict = {"amount": 0}

    def reserve_inventory(ctx: dict) -> dict:
        items = ctx.get("items", ["widget-1", "widget-2"])
        reserved["items"] = items
        print(f"  reserved: {items}")
        return {"reserved": items}

    def release_inventory(output: dict) -> None:
        reserved["items"] = []
        print(f"  released: {output.get('reserved', [])}")

    def charge_payment(ctx: dict) -> dict:
        amount = ctx.get("amount", 99.00)
        charged["amount"] = amount
        print(f"  charged: {amount}")
        return {"charged": amount}

    def refund_payment(output: dict) -> None:
        charged["amount"] = 0
        print(f"  refunded: {output.get('charged', 0)}")

    def send_confirmation(ctx: dict) -> dict:
        raise RuntimeError("email service unavailable")

    def send_cancellation(output: Any) -> None:
        print("  sent cancellation notice")

    print("--- Scenario 1: failure at step 3 → compensate steps 1+2 ---\n")
    saga = (
        Saga()
        .step("reserve_inventory", reserve_inventory, release_inventory)
        .step("charge_payment", charge_payment, refund_payment)
        .step("send_confirmation", send_confirmation, send_cancellation)
    )
    r = saga.execute({"items": ["widget-1"], "amount": 49.00})
    print(f"\nResult: success={r.success}, failed_at={r.failed_at!r}")
    print(f"Completed: {r.completed}")
    print(f"Compensated: {r.compensated}")
    assert reserved["items"] == [], "inventory should be released"
    assert charged["amount"] == 0, "payment should be refunded"

    print("\n--- Scenario 2: all steps succeed ---\n")

    def send_ok(ctx: dict) -> dict:
        print("  confirmation sent")
        return {"confirmed": True}

    saga2 = (
        Saga()
        .step("reserve_inventory", reserve_inventory, release_inventory)
        .step("charge_payment", charge_payment, refund_payment)
        .step("send_confirmation", send_ok, send_cancellation)
    )
    r2 = saga2.execute({"items": ["widget-2"], "amount": 29.00})
    print(f"\nResult: success={r2.success}, compensated={r2.compensated}")
    assert r2.success
    assert r2.compensated == []


if __name__ == "__main__":
    main()
