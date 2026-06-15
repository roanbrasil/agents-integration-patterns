from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

class OrchestratorState(TypedDict):
    topic: str
    info: str
    analysis: str
    summary: str

def step1_gather(state: OrchestratorState) -> OrchestratorState:
    topic = state["topic"]
    info = llm.invoke(f"List 3 key facts about: {topic}. Be concise.")
    print(f"[Step 1 - Gather] {info.content.strip()}")
    return {**state, "info": info.content.strip()}

def step2_analyze(state: OrchestratorState) -> OrchestratorState:
    analysis = llm.invoke(
        f"Analyze the following facts about '{state['topic']}' and identify the most important insight:\n{state['info']}"
    )
    print(f"[Step 2 - Analyze] {analysis.content.strip()}")
    return {**state, "analysis": analysis.content.strip()}

def step3_summarize(state: OrchestratorState) -> OrchestratorState:
    summary = llm.invoke(
        f"Write a 2-sentence executive summary combining facts and analysis:\nFacts: {state['info']}\nAnalysis: {state['analysis']}"
    )
    print(f"[Step 3 - Summarize] {summary.content.strip()}")
    return {**state, "summary": summary.content.strip()}

def build_graph():
    g = StateGraph(OrchestratorState)
    g.add_node("gather", step1_gather)
    g.add_node("analyze", step2_analyze)
    g.add_node("summarize", step3_summarize)
    g.set_entry_point("gather")
    g.add_edge("gather", "analyze")
    g.add_edge("analyze", "summarize")
    g.add_edge("summarize", END)
    return g.compile()

def main():
    graph = build_graph()
    initial: OrchestratorState = {
        "topic": "event-driven microservices",
        "info": "",
        "analysis": "",
        "summary": "",
    }
    result = graph.invoke(initial)
    print(f"\n[Orchestrator Done]\nSummary: {result['summary']}")

if __name__ == "__main__":
    main()
