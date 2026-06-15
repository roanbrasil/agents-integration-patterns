from langchain_anthropic import ChatAnthropic
from typing import TypedDict

# --- Agent Card Registry ---

REGISTRY: dict[str, dict] = {
    "translator_agent": {
        "name": "translator_agent",
        "version": "1.0",
        "capabilities": ["translation", "language_detection"],
        "description": "Translates text between languages",
        "endpoint": "local://translator_agent",
    },
    "summarizer_agent": {
        "name": "summarizer_agent",
        "version": "1.0",
        "capabilities": ["summarization", "extraction"],
        "description": "Summarizes long documents",
        "endpoint": "local://summarizer_agent",
    },
    "qa_agent": {
        "name": "qa_agent",
        "version": "1.0",
        "capabilities": ["question_answering", "retrieval"],
        "description": "Answers questions from context",
        "endpoint": "local://qa_agent",
    },
}


def discover_agent(capability: str) -> dict | None:
    for card in REGISTRY.values():
        if capability in card["capabilities"]:
            return card
    return None


def delegate_task(agent_card: dict, task: str) -> str:
    llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
    prompt = (
        f"You are {agent_card['name']}. {agent_card['description']}.\n"
        f"Task: {task}"
    )
    return llm.invoke(prompt).content


def main():
    required_capability = "translation"
    task = "Translate 'Hello, how are you?' to Portuguese."

    print(f"[Registry] Querying registry for capability: '{required_capability}'")
    agent_card = discover_agent(required_capability)

    if not agent_card:
        print(f"[Registry] No agent found with capability: {required_capability}")
        return

    print(f"[Registry] Found agent: {agent_card['name']} (v{agent_card['version']})")
    print(f"[Registry] Delegating task to {agent_card['endpoint']}")
    print(f"[Task] {task}")

    result = delegate_task(agent_card, task)
    print(f"[Result] {result}")


if __name__ == "__main__":
    main()
