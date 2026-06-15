from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

class SupervisionState(TypedDict):
    task: str
    subtasks: list[str]
    worker_a_result: str
    worker_b_result: str
    final_review: str

def supervisor_split(state: SupervisionState) -> SupervisionState:
    task = state["task"]
    response = llm.invoke(
        f"Split this task into exactly 2 subtasks (one line each, no numbering):\n{task}"
    )
    lines = [l.strip() for l in response.content.strip().split("\n") if l.strip()]
    subtasks = lines[:2] if len(lines) >= 2 else [task, task]
    print(f"[Supervisor] Subtasks: {subtasks}")
    return {**state, "subtasks": subtasks}

def worker_a(state: SupervisionState) -> SupervisionState:
    subtask = state["subtasks"][0]
    result = llm.invoke(f"Complete this subtask in 1-2 sentences:\n{subtask}")
    print(f"[Worker A] {result.content.strip()}")
    return {**state, "worker_a_result": result.content.strip()}

def worker_b(state: SupervisionState) -> SupervisionState:
    subtask = state["subtasks"][1]
    result = llm.invoke(f"Complete this subtask in 1-2 sentences:\n{subtask}")
    print(f"[Worker B] {result.content.strip()}")
    return {**state, "worker_b_result": result.content.strip()}

def supervisor_review(state: SupervisionState) -> SupervisionState:
    combined = f"Result A: {state['worker_a_result']}\nResult B: {state['worker_b_result']}"
    review = llm.invoke(f"Review and synthesize these two results in 2 sentences:\n{combined}")
    print(f"[Supervisor Review] {review.content.strip()}")
    return {**state, "final_review": review.content.strip()}

def build_graph():
    g = StateGraph(SupervisionState)
    g.add_node("supervisor_split", supervisor_split)
    g.add_node("worker_a", worker_a)
    g.add_node("worker_b", worker_b)
    g.add_node("supervisor_review", supervisor_review)
    g.set_entry_point("supervisor_split")
    g.add_edge("supervisor_split", "worker_a")
    g.add_edge("worker_a", "worker_b")
    g.add_edge("worker_b", "supervisor_review")
    g.add_edge("supervisor_review", END)
    return g.compile()

def main():
    graph = build_graph()
    initial = {
        "task": "Write a short report on the benefits of microservices architecture",
        "subtasks": [],
        "worker_a_result": "",
        "worker_b_result": "",
        "final_review": "",
    }
    result = graph.invoke(initial)
    print(f"\n[Final] {result['final_review']}")

if __name__ == "__main__":
    main()
