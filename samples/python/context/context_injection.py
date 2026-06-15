from langchain_anthropic import ChatAnthropic
from typing import TypedDict

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

# Simulated MCP resources
MCP_RESOURCES = {
    "user_profile": {
        "name": "Alice",
        "role": "Data Scientist",
        "preferences": "concise answers, Python examples",
    },
    "document": {
        "title": "Intro to LangGraph",
        "content": (
            "LangGraph is a library for building stateful, multi-actor applications "
            "with LLMs. It uses a graph structure where nodes are functions and edges "
            "define control flow. It supports cycles, branching, and persistence."
        ),
    },
}

def fetch_resource(name: str) -> dict:
    return MCP_RESOURCES.get(name, {})

def build_context_prompt(question: str) -> str:
    profile = fetch_resource("user_profile")
    doc = fetch_resource("document")

    context = f"""You are helping a user. Here is their profile and a reference document.

USER PROFILE:
- Name: {profile['name']}
- Role: {profile['role']}
- Preferences: {profile['preferences']}

REFERENCE DOCUMENT: {doc['title']}
{doc['content']}

USER QUESTION: {question}

Answer the question using the document context, tailored to the user's preferences."""
    return context

def main():
    question = "What is LangGraph and when should I use it?"

    print("=== Context Injection Pattern ===")
    print(f"Question: {question}\n")

    prompt = build_context_prompt(question)
    print("--- Injected Context Sent to Agent ---")
    print(prompt)
    print("\n--- Agent Response ---")

    response = llm.invoke(prompt)
    print(response.content)

if __name__ == "__main__":
    main()
