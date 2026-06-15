from typing import TypedDict, Literal
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

class State(TypedDict):
    task: str
    output: str
    verdict: str
    reason: str
    retries: int


def produce(state: State) -> State:
    attempt = state["retries"] + 1
    prompt = (
        f"Answer the following task concisely (attempt {attempt}/3):\n{state['task']}"
    )
    response = llm.invoke(prompt)
    print(f"[Producer] Attempt {attempt}: {response.content[:120]}")
    return {**state, "output": response.content}


def judge(state: State) -> State:
    prompt = (
        f"You are a strict evaluator. Given the task and answer below, "
        f"reply with exactly one word: APPROVED or REJECTED, then a dash and a short reason.\n\n"
        f"Task: {state['task']}\n"
        f"Answer: {state['output']}\n\n"
        f"Evaluation:"
    )
    response = llm.invoke(prompt)
    text = response.content.strip()
    verdict = "APPROVED" if text.upper().startswith("APPROVED") else "REJECTED"
    reason = text.split("-", 1)[-1].strip() if "-" in text else text
    print(f"[Judge] Verdict: {verdict} | Reason: {reason}")
    return {**state, "verdict": verdict, "reason": reason}


def route(state: State) -> Literal["produce", "dead_letter", "__end__"]:
    if state["verdict"] == "APPROVED":
        return "__end__"
    if state["retries"] < 2:
        return "produce"
    return "dead_letter"


def increment_retries(state: State) -> State:
    return {**state, "retries": state["retries"] + 1}


def dead_letter(state: State) -> State:
    print(f"[Dead Letter] Max retries reached. Last reason: {state['reason']}")
    return state


builder = StateGraph(State)
builder.add_node("produce", produce)
builder.add_node("judge", judge)
builder.add_node("increment", increment_retries)
builder.add_node("dead_letter", dead_letter)

builder.set_entry_point("produce")
builder.add_edge("produce", "judge")
builder.add_conditional_edges(
    "judge",
    route,
    {"__end__": END, "produce": "increment", "dead_letter": "dead_letter"},
)
builder.add_edge("increment", "produce")
builder.add_edge("dead_letter", END)

graph = builder.compile()


def main():
    task = "Explain what a REST API is in exactly one sentence."
    initial: State = {"task": task, "output": "", "verdict": "", "reason": "", "retries": 0}
    print(f"[Task] {task}\n")
    result = graph.invoke(initial)
    print(f"\n[Final] Verdict={result['verdict']} | Output={result['output'][:150]}")


if __name__ == "__main__":
    main()
