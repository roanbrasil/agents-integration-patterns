"""Magentic Orchestration Pattern — a manager maintains a task ledger and re-plans.

Framework-agnostic. The manager builds a living plan, dispatches steps to
registered specialists, folds results back into the ledger, and re-plans each
round. Stall detection + a round cap bound the (non-deterministic) execution.

Run: python3 coordination/magentic.py
See: patterns/coordination/magentic.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

Specialist = Callable[[str], str]
Planner = Callable[["TaskLedger"], list[str]]


@dataclass
class TaskLedger:
    """A living record of the emergent plan and progress."""

    goal: str
    facts: list[str] = field(default_factory=list)
    plan: list[str] = field(default_factory=list)
    done: list[tuple[str, str]] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)

    def record(self, step: str, result: str) -> None:
        self.done.append((step, result))
        self.facts.append(f"{step} -> {result}")


class MagenticManager:
    """Maintains the ledger, dispatches steps, and re-plans until done."""

    def __init__(self, planner: Planner, max_rounds: int = 8, stall_limit: int = 2):
        self.planner = planner
        self.max_rounds = max_rounds
        self.stall_limit = stall_limit
        self.specialists: dict[str, Specialist] = {}

    def register(self, name: str, specialist: Specialist) -> "MagenticManager":
        self.specialists[name] = specialist
        return self

    def run(self, goal: str) -> TaskLedger:
        ledger = TaskLedger(goal=goal)
        stalls = 0
        for _ in range(self.max_rounds):
            ledger.plan = self.planner(ledger)
            if not ledger.plan:
                return ledger
            next_step = ledger.plan[0]
            name, _, task = next_step.partition(":")
            specialist = self.specialists.get(name.strip())
            if specialist is not None:
                result = specialist(task.strip() or next_step)
                ledger.record(next_step, result)
                stalls = 0
            else:
                ledger.open_questions.append(f"no specialist for: {next_step}")
                stalls += 1
            if stalls >= self.stall_limit:
                ledger.open_questions.append("stalled — escalating")
                return ledger
        ledger.open_questions.append("round cap reached")
        return ledger


def llm_planner(ledger: TaskLedger) -> list[str]:
    done_steps = {s for s, _ in ledger.done}
    facts_text = "\n".join(ledger.facts) or "none yet"
    prompt = (
        f"You are a task planner. Goal: {ledger.goal}\n"
        f"Completed steps: {list(done_steps) or 'none'}\n"
        f"Facts gathered: {facts_text}\n"
        f"Available specialists: researcher, writer.\n"
        f"Return the NEXT step only (format: 'specialist: task') or 'DONE' if complete."
    )
    response = llm.invoke(prompt).content.strip()
    if response.upper() == "DONE" or not response:
        return []
    return [response]


def main() -> None:
    print("=== Magentic Orchestration ===\n")

    def researcher(task: str) -> str:
        r = llm.invoke(f"Research briefly (2 sentences): {task}")
        return r.content

    def writer(task: str) -> str:
        r = llm.invoke(f"Write a short section (2 sentences) about: {task}")
        return r.content

    mgr = (
        MagenticManager(planner=llm_planner, max_rounds=6, stall_limit=2)
        .register("researcher", researcher)
        .register("writer", writer)
    )

    ledger = mgr.run("produce a competitive analysis of Python vs TypeScript for AI agents")

    print(f"Goal: {ledger.goal}\n")
    print("Completed steps:")
    for step, result in ledger.done:
        print(f"  [{step}] {result[:80]}")
    if ledger.open_questions:
        print(f"\nOpen: {ledger.open_questions}")


if __name__ == "__main__":
    main()
