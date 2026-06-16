# Orchestrator

**Category:** Coordination
**Maturity:** ★★ Established
**Also known as:** Process Manager (EIP), Central Coordinator, Workflow Engine, Conductor

## Intent

A central coordinator defines the execution flow, sequences agent calls, and manages shared state — following a pre-defined plan rather than reacting to runtime monitoring.

## Context

You are building a multi-agent workflow whose steps are known in advance: a defined sequence (or branching graph) of agent invocations where each step consumes the state produced by earlier steps. You need one place that owns the plan and the state.

## Problem

Multiple agents must be coordinated in a defined order, with state passed between them and branching logic applied — but if every agent knows about every other agent, the workflow logic smears across the whole system and becomes impossible to audit, test, or change.

## Forces

- **F6 Observability vs. F9 Scalability** — centralizing the flow makes it inspectable and testable, but the coordinator becomes a throughput bottleneck and a single point of failure.
- **F8 Determinism vs. F10 Adaptability** — a fixed plan is reproducible and easy to reason about, but less able to adapt to situations the plan's author did not foresee.
- **F2 Coupling** — agents stay decoupled from *each other* (they only know the orchestrator), but each becomes coupled to the orchestrator's state schema.

The Orchestrator chooses observability and determinism over scalability and adaptability. When those priorities invert, see *Choreography*.

## Solution

The orchestrator holds the workflow graph. It calls agents in sequence or in parallel according to the plan, passes state between steps, and applies branching logic. Unlike a *Supervised Delegation* supervisor, it does not monitor agents and dynamically re-plan — it executes a plan that was fixed at design time.

State is centralized and explicit, which is what gives the pattern its auditability: at any step you can serialize and inspect the entire workflow state.

![Orchestrator](../../img/orchestrator.svg)

## Sample Code

Runnable, tested implementation: [`samples/coordination/orchestrator/`](../../samples/coordination/orchestrator/)

```python
# Excerpt — the orchestrator owns the plan and the state
graph = Orchestrator(state_schema=ResearchState)
graph.add_step("search",  search_agent)
graph.add_step("analyze", analyze_agent)
graph.add_step("report",  report_agent)
graph.add_conditional("review", review_agent,
                      on_reject="report", on_approve=END)
result = graph.run(initial={"query": "agentic AI frameworks"})
```

## Consequences

- ✅ Predictable execution; trivial to audit and unit-test each step in isolation (resolves F6, F8).
- ✅ Centralized state management — one schema, one place to inspect (resolves F6).
- ❌ The orchestrator must be updated whenever the workflow changes (introduces F10 cost).
- ❌ Becomes a bottleneck and single point of failure under load (introduces F9 cost).

## Failure Modes Mitigated

Per [FAILURE-MAP.md](../FAILURE-MAP.md):

- **FM-1.5 Unaware of termination conditions** ✅ — the plan defines explicit end states, so the system always knows when it is done.
- **FM-3.1 Premature termination** ✅ — steps cannot be skipped; the graph enforces completion before `END`.
- **FM-2.3 Task derailment** ✅ — agents cannot wander off-plan because they do not control the flow.
- **FM-1.3 Step repetition** ◐ — explicit state makes accidental repetition visible and preventable.

## Known Uses

- LangGraph `StateGraph` — the canonical implementation.
- Azure Semantic Kernel planners.
- Anthropic's "orchestrator–subagents" workflow (*Building Effective Agents*, 2024).
- AWS Step Functions used as an agent workflow engine.

## Related Patterns

- *alternative-to* **[Choreography](choreography.md)** — decentralized, event-driven; inverts the F6/F9 trade-off.
- *alternative-to* **[Supervised Delegation](supervised-delegation.md)** — adds a runtime monitoring loop; choose it when the plan must adapt to failures.
- *uses* **[Pipeline](../routing/pipeline.md)** — a linear orchestrator is a pipeline.
- *used-by* **[Checkpoint & Resume](../resilience/checkpoint-resume.md)** — centralized state is what makes checkpointing natural.

## References

- Hohpe, G. & Woolf, B. (2003). *Enterprise Integration Patterns* — Process Manager.
- Anthropic (2024). *Building Effective Agents.*
- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv:2503.13657.
