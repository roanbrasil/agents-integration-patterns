from langchain_anthropic import ChatAnthropic
from typing import Literal

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")


def router_agent(task: str) -> Literal["coding", "research", "data"]:
    prompt = (
        f"Classify this task into exactly one category: coding, research, or data.\n"
        f"Task: {task}\n"
        f"Reply with only the single word: coding, research, or data."
    )
    result = llm.invoke(prompt)
    category = result.content.strip().lower()
    for valid in ("coding", "research", "data"):
        if valid in category:
            return valid  # type: ignore
    return "research"


def coding_agent(task: str) -> str:
    return llm.invoke(f"You are a coding expert. Answer briefly: {task}").content


def research_agent(task: str) -> str:
    return llm.invoke(f"You are a research expert. Answer briefly: {task}").content


def data_agent(task: str) -> str:
    return llm.invoke(f"You are a data analyst. Answer briefly: {task}").content


SPECIALISTS = {
    "coding": coding_agent,
    "research": research_agent,
    "data": data_agent,
}


def route(task: str) -> str:
    category = router_agent(task)
    print(f"  [router] classified as: {category}")
    specialist = SPECIALISTS[category]
    return specialist(task)


def main() -> None:
    tasks = [
        "Write a Python function to reverse a linked list.",
        "What were the main causes of the French Revolution?",
        "What is the average salary in the dataset if values are 50k, 75k, 90k, 65k?",
    ]

    for task in tasks:
        print(f"\nTask: {task}")
        answer = route(task)
        print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
