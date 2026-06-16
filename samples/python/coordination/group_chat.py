"""Group Chat Pattern — a chat manager drives an accumulating thread.

Framework-agnostic. The chat manager decides who speaks next; agents react to
the shared thread. Includes the turn-based Maker-Checker specialization.

Run: python3 coordination/group_chat.py
See: patterns/coordination/group-chat.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from langchain_anthropic import ChatAnthropic

# An agent reads the thread (list of (speaker, text)) and returns its message.
Participant = Callable[[list[tuple[str, str]]], str]
# A manager picks the next speaker name given the thread, or None to stop.
Manager = Callable[[list[tuple[str, str]], list[str]], str | None]

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")


@dataclass
class GroupChat:
    """Coordinates a shared, accumulating conversation thread."""

    manager: Manager
    max_turns: int = 10
    participants: dict[str, Participant] = field(default_factory=dict)
    thread: list[tuple[str, str]] = field(default_factory=list)

    def add(self, name: str, agent: Participant) -> "GroupChat":
        self.participants[name] = agent
        return self

    def run(self, opening: str) -> list[tuple[str, str]]:
        self.thread.append(("input", opening))
        names = list(self.participants)
        for _ in range(self.max_turns):
            speaker = self.manager(self.thread, names)
            if speaker is None:
                return self.thread
            message = self.participants[speaker](self.thread)
            self.thread.append((speaker, message))
        return self.thread


def maker_checker_manager(approve_token: str = "APPROVED") -> Manager:
    """Turn-based: maker proposes, checker evaluates. Stops when checker approves."""

    def manager(thread: list[tuple[str, str]], names: list[str]) -> str | None:
        for speaker, text in reversed(thread):
            if speaker == "checker":
                if approve_token in text:
                    return None
                break
        last_speaker = thread[-1][0]
        return "checker" if last_speaker == "maker" else "maker"

    return manager


def llm_maker(thread: list[tuple[str, str]]) -> str:
    prior = [t for s, t in thread if s == "maker"]
    feedback = next((t for s, t in reversed(thread) if s == "checker"), "")
    prompt = (
        f"You are a writer. Previous drafts: {len(prior)}. "
        f"Feedback: {feedback or 'none yet'}. "
        f"Write a short improved draft (2 sentences) for: {thread[0][1]}"
    )
    return llm.invoke(prompt).content


def llm_checker(thread: list[tuple[str, str]]) -> str:
    last_draft = next((t for s, t in reversed(thread) if s == "maker"), "")
    goal = thread[0][1]
    prompt = (
        f"You are a strict reviewer. Goal: {goal}\nDraft: {last_draft}\n"
        f"If the draft fully addresses the goal, reply starting with APPROVED. "
        f"Otherwise start with REJECTED and give one line of feedback."
    )
    return llm.invoke(prompt).content


def main() -> None:
    print("=== Group Chat — Maker-Checker ===\n")
    chat = (
        GroupChat(manager=maker_checker_manager(), max_turns=8)
        .add("maker", llm_maker)
        .add("checker", llm_checker)
    )
    thread = chat.run("draft a two-sentence refund policy for a SaaS product")
    for speaker, text in thread:
        print(f"[{speaker:8}] {text[:120]}")


if __name__ == "__main__":
    main()
