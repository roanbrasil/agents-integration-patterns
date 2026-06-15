"""
Checkpoint & Resume Pattern
Persist LangGraph state after each step, resume from checkpoint on failure.
"""
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")


class PipelineState(TypedDict):
    topic: str
    step1_output: str
    step2_output: str
    step3_output: str


def step1_research(state: PipelineState) -> PipelineState:
    print("[step1] Researching topic...")
    response = llm.invoke(f"In one sentence, define: {state['topic']}")
    out = response.content if hasattr(response, "content") else str(response)
    print(f"[step1] Output: {out}")
    return {**state, "step1_output": out}


def step2_analyze(state: PipelineState) -> PipelineState:
    print("[step2] Analyzing research...")
    response = llm.invoke(f"List 2 key challenges related to: {state['step1_output']}")
    out = response.content if hasattr(response, "content") else str(response)
    print(f"[step2] Output: {out}")
    return {**state, "step2_output": out}


def step3_summarize(state: PipelineState) -> PipelineState:
    print("[step3] Summarizing analysis...")
    response = llm.invoke(f"In one sentence, summarize this analysis: {state['step2_output']}")
    out = response.content if hasattr(response, "content") else str(response)
    print(f"[step3] Output: {out}")
    return {**state, "step3_output": out}


def build_graph(checkpointer: MemorySaver) -> StateGraph:
    graph = StateGraph(PipelineState)
    graph.add_node("step1", step1_research)
    graph.add_node("step2", step2_analyze)
    graph.add_node("step3", step3_summarize)
    graph.set_entry_point("step1")
    graph.add_edge("step1", "step2")
    graph.add_edge("step2", "step3")
    graph.add_edge("step3", END)
    return graph.compile(checkpointer=checkpointer)


def main():
    memory = MemorySaver()
    app = build_graph(memory)
    thread_id = "pipeline-run-001"
    config = {"configurable": {"thread_id": thread_id}}

    initial_state: PipelineState = {
        "topic": "resilience patterns in distributed systems",
        "step1_output": "",
        "step2_output": "",
        "step3_output": "",
    }

    print("=== Initial Run (full pipeline) ===")
    output = app.invoke(initial_state, config=config)
    print(f"\nPipeline complete.")
    print(f"Final summary: {output['step3_output']}")

    print("\n=== Simulating Resume from Checkpoint ===")
    saved = app.get_state(config)
    print(f"Checkpoint found at thread_id='{thread_id}'")
    print(f"Checkpoint values keys: {list(saved.values.keys())}")
    print(f"Next nodes: {saved.next if saved.next else ['(pipeline finished)']}")

    resumed = app.invoke(None, config=config)
    print(f"\nResumed pipeline step3_output: {resumed['step3_output']}")
    print("Resume from checkpoint demonstrated successfully.")


if __name__ == "__main__":
    main()
