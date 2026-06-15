# Pipeline

> Pass a task through a sequence of agents, where each agent transforms or enriches the result before passing it to the next.

**Category:** routing
**EIP Analog:** [Pipes and Filters](https://www.enterpriseintegrationpatterns.com/patterns/messaging/PipesAndFilters.html)

---

## Also Known As

Agent Chain, Prompt Chain, Sequential Workflow

---

## Problem

A complex task requires a series of transformations where each step depends on the previous result: extract, then analyze, then format, then verify. Putting all logic in one agent makes it unfocused and hard to test. Running steps in parallel is incorrect because they have data dependencies.

---

## Solution

Chain agents as pipeline stages. Each agent (filter) has a focused responsibility. It receives the output of the previous stage, transforms or enriches it, and passes the result to the next stage. The pipeline as a whole transforms raw input into a final output.

---

## Diagram

```
 Input ──► Agent A ──► Agent B ──► Agent C ──► Output
           (Extract)  (Analyze)  (Format)
              │           │          │
           focused     focused    focused
```

---

## Participants

| Participant | Role |
|---|---|
| **Source** | Provides the initial input |
| **Filter Agents** | Each stage transforms the data; focused on one responsibility |
| **Sink** | Consumes the final output |
| **Pipeline Runner** | Coordinates passing state between stages (orchestrator, LangGraph, etc.) |

---

## Consequences

**Benefits:**
- ✅ Each stage is independently testable and replaceable
- ✅ Easy to insert, remove, or reorder stages
- ✅ Clear data flow — easy to trace and debug

**Trade-offs:**
- ❌ Sequential — total latency is the sum of all stage latencies
- ❌ A failure in an early stage cascades through all downstream stages
- ❌ Context can be lost between stages if state management is not careful

---

## Implementation

```python
# Pipeline using LangGraph as the runner
from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-6")

class PipelineState(TypedDict):
    raw_text: str
    extracted_data: dict
    analysis: str
    final_report: str

def extract_agent(state: PipelineState) -> PipelineState:
    response = llm.invoke(
        f"Extract key entities (people, dates, amounts) as JSON from:\n{state['raw_text']}"
    )
    return {"extracted_data": {"raw": response.content}}

def analyze_agent(state: PipelineState) -> PipelineState:
    response = llm.invoke(
        f"Analyze the significance of this extracted data:\n{state['extracted_data']}"
    )
    return {"analysis": response.content}

def format_agent(state: PipelineState) -> PipelineState:
    response = llm.invoke(
        f"Format this analysis as an executive summary:\n{state['analysis']}"
    )
    return {"final_report": response.content}

graph = StateGraph(PipelineState)
graph.add_node("extract", extract_agent)
graph.add_node("analyze", analyze_agent)
graph.add_node("format", format_agent)

graph.set_entry_point("extract")
graph.add_edge("extract", "analyze")
graph.add_edge("analyze", "format")
graph.add_edge("format", END)
```

---

## Known Uses

- **Anthropic "Prompt Chaining"** — the canonical agentic workflow where each LLM call feeds the next
- **LangGraph linear graphs** — sequential node chains are the simplest LangGraph topology
- **CrewAI Sequential Process** — tasks executed one after another with output passed as context to the next
- **Data processing pipelines** — ETL-style agent chains: fetch → clean → embed → store

---

## Related Patterns

- [Scatter-Gather](./scatter-gather.md) — use when pipeline stages can run in parallel
- [Checkpoint & Resume](../resilience/checkpoint-resume.md) — persist state between stages for long pipelines
- [Orchestrator](../coordination/orchestrator.md) — the pipeline runner is a lightweight orchestrator

---

## References

- Hohpe & Woolf (2003). *Enterprise Integration Patterns*: Pipes and Filters
- [Anthropic: Building Effective Agents — Prompt Chaining](https://www.anthropic.com/research/building-effective-agents)
