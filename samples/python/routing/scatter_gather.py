from langchain_anthropic import ChatAnthropic
from typing import TypedDict

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

AGENT_ROLES = [
    "optimist who highlights benefits and opportunities",
    "skeptic who raises concerns and risks",
    "pragmatist who focuses on practical implementation steps",
]


def agent_perspective(question: str, role: str) -> str:
    prompt = (
        f"You are a {role}. In 2-3 sentences, share your perspective on:\n{question}"
    )
    return llm.invoke(prompt).content


def scatter(question: str) -> list[str]:
    return [agent_perspective(question, role) for role in AGENT_ROLES]


def gather(question: str, perspectives: list[str]) -> str:
    joined = "\n\n".join(
        f"Perspective {i + 1} ({AGENT_ROLES[i]}):\n{p}"
        for i, p in enumerate(perspectives)
    )
    prompt = (
        f"Synthesize these 3 perspectives on '{question}' into one balanced summary "
        f"(3-4 sentences):\n\n{joined}"
    )
    return llm.invoke(prompt).content


def scatter_gather(question: str) -> str:
    print(f"\nQuestion: {question}")
    perspectives = scatter(question)
    for i, (role, view) in enumerate(zip(AGENT_ROLES, perspectives)):
        print(f"\n  [{i + 1}] {role.capitalize()}:\n  {view}")
    summary = gather(question, perspectives)
    return summary


def main() -> None:
    question = "Should companies adopt AI-driven hiring processes?"
    synthesis = scatter_gather(question)
    print(f"\n--- Synthesis ---\n{synthesis}")


if __name__ == "__main__":
    main()
