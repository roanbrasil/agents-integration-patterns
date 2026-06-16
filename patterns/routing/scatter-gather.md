# Scatter-Gather
**Category:** Routing
**Maturity:** ★★ Established
**Also known as:** Fan-Out/Fan-In, Map-Reduce, Concurrent Agents, Parallel Perspectives

> Send the same task to multiple agents in parallel, then aggregate their responses into a single coherent result.

**EIP Analog:** [Scatter-Gather](https://www.enterpriseintegrationpatterns.com/patterns/messaging/BroadcastAggregate.html)

---

## Intent

Fan out a single task to N independent agents running in parallel, then aggregate their independent responses into one consolidated result — combining the quality benefits of multiple perspectives with the latency benefits of parallelism.

---

## Context

Some tasks benefit from multiple independent perspectives, and sequential querying is too slow. You need parallel execution across multiple agents but a single coherent result returned to the caller.

---

## Problem

Some tasks benefit from multiple independent perspectives. Sequential querying of agents is slow, and a single agent's answer may have blind spots, biases, or errors. You need parallel execution across multiple agents but a single coherent result.

---

## Forces

- **F4 Answer quality vs. F3 Token cost / F1 Latency** — multiple independent perspectives improve quality but cost N× tokens and run in parallel (wall-clock = slowest agent, not sum).
- **F9 Scalability** — agents run in parallel; adding more agents increases quality without increasing wall-clock time (to a point).
- **F2 Coupling** — the scatter step is a broadcast; the gather step is an aggregation; neither knows about the other's implementation.

---

## Solution

A dispatcher sends the same task to N agents simultaneously. Each agent processes independently without awareness of the others. A gatherer waits for all responses (or a timeout) and passes them to a synthesis step — which may vote, merge, rank, or use a final agent to produce the consolidated answer.

---

## Diagram

![Scatter-Gather — Dispatch fans out to Agent A, B, and C in parallel, results flow into Aggregate](../../img/Scatter-Gather.png)

---

## Participants

| Participant | Role |
|---|---|
| **Dispatcher** | Sends identical (or parameterized) tasks to all agents simultaneously |
| **Worker Agents** | Process the task independently; unaware of parallel execution |
| **Aggregator** | Collects results and synthesizes a final answer (majority vote, LLM synthesis, etc.) |

---

## Sample Code

Runnable implementation: [samples/python/routing/scatter_gather.py](../../samples/python/routing/scatter_gather.py)

```python
# Scatter-Gather with LangGraph parallel nodes
import asyncio
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

llm = ChatAnthropic(model="claude-sonnet-4-6")

class ScatterState(TypedDict):
    task: str
    responses: Annotated[list[str], operator.add]
    final_answer: str

async def agent_perspective(state: ScatterState, persona: str) -> dict:
    response = await llm.ainvoke(
        f"You are a {persona}. Answer this: {state['task']}"
    )
    return {"responses": [response.content]}

async def scatter(state: ScatterState) -> dict:
    results = await asyncio.gather(
        agent_perspective(state, "skeptic"),
        agent_perspective(state, "optimist"),
        agent_perspective(state, "domain expert"),
    )
    combined = []
    for r in results:
        combined.extend(r["responses"])
    return {"responses": combined}

def gather(state: ScatterState) -> dict:
    combined = "\n\n---\n\n".join(
        f"Perspective {i+1}:\n{r}" for i, r in enumerate(state["responses"])
    )
    synthesis = llm.invoke(
        f"Synthesize these perspectives into one coherent answer:\n\n{combined}"
    )
    return {"final_answer": synthesis.content}
```

---

## Consequences

- ✅ Multiple independent perspectives — higher quality than single agent (F4 resolved)
- ✅ Parallelism — wall-clock time = slowest agent, not sum (F9 resolved)
- ✅ Naturally fault-tolerant — if one agent fails, the majority can still produce a result
- ❌ N× token cost (F3 introduced)
- ❌ Aggregation step may lose nuance present in individual responses
- ❌ Requires careful timeout handling when some agents are slower than others

---

## When to avoid

- When one specialist is clearly right — scatter to wrong agents adds noise.
- When real-time latency budgets cannot absorb waiting for the slowest agent.
- When cross-agent discussion is needed — use Group Chat instead.

---

## Failure Modes Mitigated

Per [FAILURE-MAP.md](../FAILURE-MAP.md):
- **FM-2.4 Information withholding** ✅ — all agents receive the same question; no perspective is excluded.
- **FM-3.2 No or incomplete verification** ◐ — multiple independent answers improve coverage (though not a verification gate).

---

## Known Uses

- **Multi-Agent Debate (Google DeepMind)** — multiple LLM instances debate a question; a judge synthesizes the winning argument
- **Anthropic's "Parallelization" workflow** — scatter identical tasks across multiple subagents and aggregate results
- **LLM-as-judge ensembles** — scatter an evaluation task to multiple LLM judges and take the majority verdict

---

## Related Patterns

- *alternative-to* [Group Chat](../coordination/group-chat.md) — parallel independent perspectives vs. cross-talking discussion.
- *alternative-to* [Content-Based Router](content-based-router.md) — fan-out to all vs. route to one.
- *refines-into* [Ensemble Judge](../evaluation/ensemble-judge.md) — when the scatter targets are judges, this becomes an ensemble.

---

## References

- Hohpe, G. & Woolf, B. (2003). *Enterprise Integration Patterns* — Scatter-Gather.
- Microsoft (2026). *AI Agent Orchestration Patterns* — Concurrent.
- Cemri, M. et al. (2025). arXiv:2503.13657.
- Du et al. (2023). "Improving Factuality and Reasoning in Language Models through Multiagent Debate." arXiv:2305.14325
- [Anthropic: Building Effective Agents — Parallelization](https://www.anthropic.com/research/building-effective-agents)
