"""Mediator Agent Pattern — all inter-agent communication routed through one node.

Eliminates N² agent-to-agent dependencies. The mediator routes messages,
maintains shared context, and synthesizes responses.

Run: python3 coordination/mediator.py
See: patterns/coordination/mediator.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

AgentFn = Callable[[str, list[str]], str]


@dataclass
class Message:
    sender: str
    content: str


@dataclass
class MediatorAgent:
    """Routes all inter-agent communication; maintains shared context."""

    max_rounds: int = 6
    _agents: dict[str, AgentFn] = field(default_factory=dict)
    _context: list[Message] = field(default_factory=list)

    def register(self, name: str, fn: AgentFn) -> "MediatorAgent":
        self._agents[name] = fn
        return self

    def _context_lines(self) -> list[str]:
        return [f"{m.sender}: {m.content}" for m in self._context]

    def send(self, to: str, content: str, sender: str = "mediator") -> str:
        self._context.append(Message(sender=sender, content=content))
        agent = self._agents[to]
        response = agent(content, self._context_lines())
        self._context.append(Message(sender=to, content=response))
        return response

    def coordinate(self, goal: str) -> str:
        self._context.clear()
        self._context.append(Message(sender="goal", content=goal))
        print(f"[mediator] goal: {goal}\n")

        names = list(self._agents.keys())
        last_result = ""
        for i, name in enumerate(names[: self.max_rounds]):
            task = goal if i == 0 else f"Given context so far, continue: {goal}"
            resp = self.send(to=name, content=task)
            print(f"[{name}] {resp[:100]}")
            last_result = resp

        return last_result

    @property
    def context(self) -> list[Message]:
        return list(self._context)


def make_researcher() -> AgentFn:
    def researcher(task: str, ctx: list[str]) -> str:
        prior = len([c for c in ctx if "researcher" in c])
        return (
            f"[Research #{prior + 1}] Key finding on '{task}': "
            "distributed systems require consensus protocols."
        )

    return researcher


def make_writer() -> AgentFn:
    def writer(task: str, ctx: list[str]) -> str:
        research = next(
            (c.split(": ", 1)[1] for c in reversed(ctx) if c.startswith("researcher")), ""
        )
        return (
            f"[Draft] Based on '{research[:60]}...', here is the summary: "
            "distributed consensus enables reliable agent coordination."
        )

    return writer


def make_critic() -> AgentFn:
    def critic(task: str, ctx: list[str]) -> str:
        draft = next(
            (c.split(": ", 1)[1] for c in reversed(ctx) if c.startswith("writer")), ""
        )
        return (
            f"[Review] Draft looks good. "
            "Suggest adding: specific protocols (Raft, Paxos) for credibility."
        )

    return critic


def main() -> None:
    print("=== Mediator Agent Pattern ===\n")
    mediator = (
        MediatorAgent(max_rounds=3)
        .register("researcher", make_researcher())
        .register("writer", make_writer())
        .register("critic", make_critic())
    )
    result = mediator.coordinate("write a research summary on agent coordination protocols")
    print(f"\nFinal result: {result}")
    print(f"Total messages through mediator: {len(mediator.context)}")


if __name__ == "__main__":
    main()
