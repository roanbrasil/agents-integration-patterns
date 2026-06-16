# Ensemble Judge

**Category:** Evaluation
**Maturity:** ★ Emerging
**Also known as:** Multi-Judge Voting, Judge Panel, Jury

## Intent

Send an agent's output to multiple independent judge agents simultaneously and determine the final verdict by majority vote.

## Context

You have an automated quality gate (see *LLM-as-Judge*) but the stakes are high enough that a single judge's bias, inconsistency, or blind spot is an unacceptable risk.

## Problem

A single LLM judge is unreliable for high-stakes quality gates. It can be systematically biased toward certain output styles, inconsistent across runs, or simply wrong in a way that correlates with the producer's own errors. Trusting one judge reintroduces the verification failures you were trying to eliminate.

## Forces

- **F4 Reliability vs. F3 Token cost / F1 Latency** — more independent judges raise reliability, but cost and latency scale linearly with the number of judges (N× a single judge).
- **F4 Reliability internal tension** — judges must be *genuinely independent* (different rubrics or lenses) for voting to help; correlated judges share blind spots and the ensemble provides false confidence.

Ensemble Judge spends N× cost and latency (F3, F1) to buy reliability (F4) — but only earns it if judge independence is real.

## Solution

Fan out the output to N independent judge agents in parallel, each evaluating through a distinct lens (e.g. correctness, safety, relevance). Apply a voting rule: ≥ M of N approvals → accepted. Disagreement (a split vote) is itself a signal — route it to human review rather than forcing a verdict.

Independence is the load-bearing requirement: judges with *different rubrics* are what make the majority vote meaningful. Three judges running the identical prompt are one judge with extra steps.

![Ensemble Judge](../../img/ensemble-judge.svg)

## Sample Code

Runnable, tested implementation: [`samples/evaluation/ensemble_judge/`](../../samples/evaluation/ensemble_judge/)

```python
# Excerpt — independent rubrics, parallel, majority vote
verdicts = await gather(
    judge("correctness", rubric_correctness, task, output),
    judge("safety",      rubric_safety,      task, output),
    judge("relevance",   rubric_relevance,   task, output),
)
approvals = sum(v.approved for v in verdicts)
result = decide(approvals, n=3, min_approvals=2)   # may be ESCALATED on a split
```

## Consequences

- ✅ Significantly more reliable than a single judge — systematic bias must corrupt the *majority* to pass (resolves F4).
- ✅ Disagreement rate is a free uncertainty signal that drives human escalation.
- ❌ N× the cost and latency of a single LLM-as-Judge (introduces F3, F1).
- ❌ A shared blind spot across all judges defeats the vote — independence is assumed, not guaranteed.

## Failure Modes Mitigated

Per [FAILURE-MAP.md](../FAILURE-MAP.md):

- **FM-3.2 No or incomplete verification** ✅ — multiple lenses cover dimensions a single judge misses.
- **FM-3.3 Incorrect verification** ✅ — a single wrong judge is outvoted.
- **FM-3.1 Premature termination** ✅ — output cannot proceed until the vote passes.
- **FM-1.1 Disobey task specification** ✅ — a dedicated correctness judge checks output against the spec.

This pattern targets the entire **Task Verification & Termination** category of MAST — the failure category single-agent systems most often lack any defense against.

## Known Uses

- Multi-agent debate (Google DeepMind).
- HELM evaluation panels (Stanford).
- Constitutional AI critique ensembles (Anthropic).

## Related Patterns

- *refines* **[LLM-as-Judge](llm-as-judge.md)** — the single-judge building block this pattern hardens.
- *specializes* **[Scatter-Gather](../routing/scatter-gather.md)** — Ensemble Judge is Scatter-Gather applied to evaluation.
- *uses* **[Dead Letter Agent](../resilience/dead-letter-agent.md)** — the escalation target for split verdicts and rejections.

## References

- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv:2503.13657.
- Bai, Y. et al. (2022). *Constitutional AI.* Anthropic.
- Liang, P. et al. *Holistic Evaluation of Language Models (HELM).* Stanford CRFM.
