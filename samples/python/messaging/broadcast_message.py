from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

SUBSCRIBER_ROLES = [
    ("Optimist",  "React with enthusiasm and highlight the positive aspects."),
    ("Skeptic",   "React with critical questions and point out potential issues."),
    ("Historian", "React by connecting this to a historical parallel or precedent."),
]


def publisher() -> str:
    """Publisher agent generates a broadcast topic sentence."""
    prompt = "Write one sentence announcing a major fictional technology breakthrough."
    topic = llm.invoke(prompt).content
    return topic


def subscriber(role: str, instruction: str, message: str) -> str:
    """Subscriber agent reacts to the broadcast message according to its role."""
    prompt = (
        f"You are a {role}. {instruction}\n"
        f"Respond in 1-2 sentences to this announcement: {message}"
    )
    return llm.invoke(prompt).content


def main():
    print("=== Broadcast Message Pattern ===\n")

    topic = publisher()
    print(f"[Publisher] Broadcast: {topic}\n")

    reactions = [
        (role, subscriber(role, instruction, topic))
        for role, instruction in SUBSCRIBER_ROLES
    ]

    print("--- Subscriber Reactions ---")
    for role, reaction in reactions:
        print(f"[{role}]: {reaction}\n")


if __name__ == "__main__":
    main()
