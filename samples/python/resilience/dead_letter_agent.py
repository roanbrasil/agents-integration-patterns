"""
Dead Letter Agent Pattern
Failed agent tasks are routed to a dead letter handler.
"""
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")


class AgentState(TypedDict):
    task: str
    result: str
    error: str
    retries: int
    status: str


def agent_node(state: AgentState) -> AgentState:
    retries = state.get("retries", 0)
    print(f"[agent_node] Attempt #{retries + 1} for task: '{state['task']}'")

    if retries < 1:
        print("[agent_node] Simulating failure on first attempt.")
        return {**state, "error": "Simulated transient failure", "retries": retries + 1, "status": "failed"}

    response = llm.invoke(f"Complete this task in one sentence: {state['task']}")
    result = response.content if hasattr(response, "content") else str(response)
    print(f"[agent_node] Task completed: {result}")
    return {**state, "result": result, "retries": retries + 1, "status": "done"}


def dead_letter_node(state: AgentState) -> AgentState:
    print(f"[dead_letter_node] Task routed to dead letter queue.")
    print(f"[dead_letter_node] Failed task: '{state['task']}'")
    print(f"[dead_letter_node] Error: {state['error']}")
    notification = (
        f"DEAD LETTER NOTIFICATION: Task '{state['task']}' "
        f"failed after {state['retries']} attempt(s). Error: {state['error']}"
    )
    print(f"[dead_letter_node] {notification}")
    return {**state, "result": notification, "status": "dead_letter"}


def route(state: AgentState) -> Literal["dead_letter_node", "agent_node", "__end__"]:
    if state["status"] == "done":
        return END
    if state["status"] == "failed" and state["retries"] >= 2:
        return "dead_letter_node"
    if state["status"] == "failed":
        return "agent_node"
    return END


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)
    graph.add_node("agent_node", agent_node)
    graph.add_node("dead_letter_node", dead_letter_node)
    graph.set_entry_point("agent_node")
    graph.add_conditional_edges("agent_node", route)
    graph.add_edge("dead_letter_node", END)
    return graph.compile()


def main():
    app = build_graph()

    print("=== Run 1: Task succeeds on retry ===")
    state1: AgentState = {"task": "Summarize the benefits of resilience patterns", "result": "", "error": "", "retries": 0, "status": "pending"}
    output1 = app.invoke(state1)
    print(f"Final status: {output1['status']}\n")

    print("=== Run 2: Task fails and goes to dead letter (force 2 failures) ===")
    state2: AgentState = {"task": "A task that will fail", "result": "", "error": "Simulated transient failure", "retries": 1, "status": "failed"}
    output2 = app.invoke(state2)
    print(f"Final status: {output2['status']}")
    print(f"Dead letter result: {output2['result']}")


if __name__ == "__main__":
    main()
