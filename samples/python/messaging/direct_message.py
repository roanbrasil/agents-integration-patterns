from typing import TypedDict
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")


class State(TypedDict):
    question: str
    answer: str


def agent_a(state: State) -> State:
    """Agent A generates a trivia question."""
    prompt = "Generate one short trivia question about space exploration. Just the question, no answer."
    question = llm.invoke(prompt).content
    print(f"[Agent A] Question: {question}")
    return {"question": question, "answer": ""}


def agent_b(state: State) -> State:
    """Agent B receives the question and answers it."""
    prompt = f"Answer this trivia question briefly (one sentence): {state['question']}"
    answer = llm.invoke(prompt).content
    print(f"[Agent B] Answer: {answer}")
    return {"answer": answer}


def main():
    print("=== Direct Message Pattern ===\n")

    graph = StateGraph(State)
    graph.add_node("agent_a", agent_a)
    graph.add_node("agent_b", agent_b)
    graph.set_entry_point("agent_a")
    graph.add_edge("agent_a", "agent_b")
    graph.add_edge("agent_b", END)

    app = graph.compile()
    result = app.invoke({"question": "", "answer": ""})

    print("\n--- Final State ---")
    print(f"Question : {result['question']}")
    print(f"Answer   : {result['answer']}")


if __name__ == "__main__":
    main()
