from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")


def agent_a(blackboard: dict) -> None:
    """Agent A writes a problem statement to the blackboard."""
    prompt = "State a short, interesting unsolved problem in computer science (2-3 sentences)."
    problem = llm.invoke(prompt).content
    blackboard["problem"] = problem
    print(f"[Agent A] Wrote problem:\n{problem}\n")


def agent_b(blackboard: dict) -> None:
    """Agent B reads the problem and writes a partial solution."""
    problem = blackboard.get("problem", "")
    prompt = (
        f"Given this problem: {problem}\n"
        "Propose one partial approach or direction toward a solution (2-3 sentences)."
    )
    partial = llm.invoke(prompt).content
    blackboard["partial_solution"] = partial
    print(f"[Agent B] Wrote partial solution:\n{partial}\n")


def agent_c(blackboard: dict) -> None:
    """Agent C reads problem and partial solution, writes a conclusion."""
    problem = blackboard.get("problem", "")
    partial = blackboard.get("partial_solution", "")
    prompt = (
        f"Problem: {problem}\n"
        f"Partial solution proposed: {partial}\n"
        "Write a brief conclusion summarizing the state of this problem and the approach (2-3 sentences)."
    )
    conclusion = llm.invoke(prompt).content
    blackboard["conclusion"] = conclusion
    print(f"[Agent C] Wrote conclusion:\n{conclusion}\n")


def main():
    print("=== Blackboard Pattern ===\n")

    blackboard: dict = {}

    agent_a(blackboard)
    agent_b(blackboard)
    agent_c(blackboard)

    print("--- Final Blackboard State ---")
    for key, value in blackboard.items():
        print(f"[{key}]:\n{value}\n")


if __name__ == "__main__":
    main()
