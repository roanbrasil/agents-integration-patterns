from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from typing import TypedDict

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")


class PipelineState(TypedDict):
    task: str
    plan: str
    result: str
    verified: str


def planner(state: PipelineState) -> PipelineState:
    prompt = (
        f"Create a brief step-by-step plan (3 steps max) to accomplish:\n{state['task']}"
    )
    plan = llm.invoke(prompt).content
    print(f"\n[planner]\n{plan}")
    return {**state, "plan": plan}


def executor(state: PipelineState) -> PipelineState:
    prompt = (
        f"Task: {state['task']}\nPlan:\n{state['plan']}\n\n"
        f"Execute the plan and provide the result in 2-3 sentences."
    )
    result = llm.invoke(prompt).content
    print(f"\n[executor]\n{result}")
    return {**state, "result": result}


def verifier(state: PipelineState) -> PipelineState:
    prompt = (
        f"Task: {state['task']}\nResult: {state['result']}\n\n"
        f"Verify whether the result adequately addresses the task. "
        f"Reply with PASS or FAIL and a one-sentence reason."
    )
    verified = llm.invoke(prompt).content
    print(f"\n[verifier]\n{verified}")
    return {**state, "verified": verified}


def build_pipeline() -> StateGraph:
    graph = StateGraph(PipelineState)
    graph.add_node("planner", planner)
    graph.add_node("executor", executor)
    graph.add_node("verifier", verifier)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "verifier")
    graph.add_edge("verifier", END)
    return graph.compile()


def main() -> None:
    task = "Explain how to set up a Python virtual environment and install dependencies."
    print(f"Task: {task}")
    pipeline = build_pipeline()
    final_state = pipeline.invoke(
        {"task": task, "plan": "", "result": "", "verified": ""}
    )
    print(f"\n--- Pipeline Complete ---")
    print(f"Verification: {final_state['verified']}")


if __name__ == "__main__":
    main()
