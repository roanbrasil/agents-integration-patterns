# LLM-as-Judge

> Route an agent's output through a dedicated judge agent that evaluates quality and decides whether to approve, reject, or escalate.

**Category:** evaluation
**EIP Analog:** [Message Validator](https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessageValidator.html) + [Content-Based Router](https://www.enterpriseintegrationpatterns.com/patterns/messaging/ContentBasedRouter.html)

---

## Also Known As

Agent Evaluator, Output Validator, Quality Gate

---

## Problem

An agent produces output that may be incorrect, incomplete, or unsafe. You cannot trust the output blindly, but human review of every response is too slow and expensive. You need an automated quality gate between production and consumption.

---

## Solution

Route the agent's output through a Judge Agent — a separate LLM invocation with a focused evaluation prompt. The judge scores or classifies the output and routes accordingly: approved outputs proceed to the next step; rejected outputs trigger a retry or escalate to the [Dead Letter Agent](../resilience/dead-letter-agent.md).

---

## Diagram

![LLM-as-Judge — Agent A produces output, Judge Agent evaluates it: APPROVED flows to next step, REJECTED triggers retry or Dead Letter Agent](../../img/llm-as-judge.png)

---

## Participants

| Participant | Role |
|---|---|
| **Producer Agent** | Generates the output to be evaluated |
| **Judge Agent** | Evaluates the output against defined criteria; returns verdict + reasoning |
| **Next Step** | Consumes approved output |
| **Retry / Dead Letter Agent** | Handles rejected output |

---

## Consequences

**Benefits:**
- ✅ Automated quality gate without human review on every request
- ✅ Judge is independently tunable — swap evaluation criteria without changing the producer
- ✅ Verdict reasoning is auditable and explainable

**Trade-offs:**
- ❌ Adds latency and cost — an extra LLM call per evaluation
- ❌ Judge can be wrong (LLM evaluators are probabilistic); critical paths may still need human review
- ❌ Judge prompt quality determines gate quality — poorly designed rubrics produce noisy verdicts

---

## Implementation

```python
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

llm = ChatAnthropic(model="claude-sonnet-4-6")
judge_llm = ChatAnthropic(model="claude-haiku-4-5-20251001")  # fast, cheap judge

class JudgeState(TypedDict):
    task: str
    output: str
    verdict: str
    retries: int

def producer_agent(state: JudgeState) -> JudgeState:
    response = llm.invoke(state["task"])
    return {"output": response.content}

def judge_agent(state: JudgeState) -> JudgeState:
    verdict = judge_llm.invoke(
        f"Evaluate this output for the task.\n\n"
        f"Task: {state['task']}\n"
        f"Output: {state['output']}\n\n"
        f"Reply with exactly APPROVED or REJECTED, then a one-line reason."
    )
    verdict_text = verdict.content.strip()
    return {"verdict": "APPROVED" if verdict_text.startswith("APPROVED") else "REJECTED"}

def route_verdict(state: JudgeState) -> Literal["approved", "retry", "dead_letter"]:
    if state["verdict"] == "APPROVED":
        return "approved"
    if state.get("retries", 0) < 2:
        return "retry"
    return "dead_letter"

graph = StateGraph(JudgeState)
graph.add_node("produce", producer_agent)
graph.add_node("judge", judge_agent)
graph.add_node("dead_letter", lambda s: s)

graph.set_entry_point("produce")
graph.add_edge("produce", "judge")
graph.add_conditional_edges("judge", route_verdict, {
    "approved": END,
    "retry": "produce",
    "dead_letter": "dead_letter",
})
graph.add_edge("dead_letter", END)
```

---

## Known Uses

- **Anthropic's agent cookbook** — recommends a separate evaluator LLM call to verify agent outputs before using them in downstream steps
- **LangSmith evaluators** — off-the-shelf LLM judges for correctness, relevance, and toxicity used in CI eval pipelines
- **OpenAI Evals framework** — LLM-as-judge is a first-class evaluation method in the evals framework

---

## Related Patterns

- [Ensemble Judge](./ensemble-judge.md) — use when a single judge is not reliable enough; N judges, majority vote
- [Dead Letter Agent](../resilience/dead-letter-agent.md) — the escalation target for permanently rejected outputs
- [Pipeline](../routing/pipeline.md) — LLM-as-Judge is typically a node in a pipeline, not a standalone pattern
- [Scatter-Gather](../routing/scatter-gather.md) — Ensemble Judge is a specialization of Scatter-Gather for evaluation

---

## References

- Zheng et al. (2023). "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." arXiv:2306.05685
- [LangSmith: LLM-as-judge evaluators](https://docs.smith.langchain.com/evaluation/how_to_guides/llm_as_judge)
