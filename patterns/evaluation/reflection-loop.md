# Reflection Loop

> An agent iteratively generates output, evaluates it against explicit criteria, and revises until the criteria are satisfied or an iteration limit is reached.

**Category:** evaluation
**Maturity:** ★ Emerging
**Also known as:** Evaluator-Optimizer, Critic-Generator Loop, Generate-Evaluate-Revise

---

## Also Known As

Evaluator-Optimizer (MindStudio, 2025), Critic-Generator Loop (MindStudio Harness Engineering, 2025), Self-Refinement (Madaan et al. 2023).

---

## Problem

An agent produces output in a single pass, but the quality of that output often depends on criteria that are only evaluable *after* generation — structural completeness, factual coverage, rubric alignment. Without a feedback loop, the agent either over-relies on prompt engineering to get it right the first time, or under-delivers on complex tasks that require iterative refinement.

The core tension: how do you get high-quality, criteria-satisfying output without a human in the review loop on every request?

---

## Forces

- **F4 Answer quality vs. F3 Token cost / F1 Latency** — each revision cycle adds latency and token spend; the benefit is measurably higher output quality on complex tasks.
- **F8 Determinism vs. F10 Adaptability** — a loop that runs until criteria are met is adaptive, but requires a precise stopping condition (F8) to prevent infinite loops.
- **Loop completion specificity (F12)** — vague exit criteria cause agents to either terminate prematurely ("close enough") or loop indefinitely. The exit condition is the load-bearing design decision.

---

## Solution

Decompose the task into two roles: a **Generator** that produces output and a **Critic** that evaluates it against an explicit rubric. Run them in a loop:

1. Generator produces initial output.
2. Critic evaluates against explicit criteria and returns a verdict (pass/fail) plus structured feedback.
3. If pass → exit loop and deliver output.
4. If fail → Generator receives critique and revises.
5. If iteration limit reached without passing → escalate to Dead Letter Agent or return best attempt with a quality flag.

The Generator and Critic can be the same model (self-critique) or different models/agents (external judgment). External Critic provides independence; self-critique is cheaper but shares the Generator's blind spots.

**The exit condition is the critical design surface.** Vague criteria ("the output is good") produce runaway loops or premature stops. Precise criteria ("the report contains an executive summary, three supporting sections each with at least two data citations, and passes relevance check") are verifiable by the Critic.

---

## Diagram

<!-- TODO: replace with PNG once img/reflection-loop.png is generated -->

```
┌─────────────────────────────────────────────────────┐
│                   Reflection Loop                    │
│                                                      │
│   Task ──► Generator ──► Draft Output               │
│                               │                      │
│                               ▼                      │
│                           Critic                     │
│                         (Rubric eval)                │
│                          │        │                  │
│                        PASS      FAIL                │
│                          │        │                  │
│                          ▼        ▼                  │
│                       Output   Critique ──► Generator│
│                                  (loop)              │
│                                                      │
│   Iteration limit ──► Dead Letter Agent              │
└─────────────────────────────────────────────────────┘
```

---

## Participants

| Participant | Role |
|---|---|
| **Generator** | Produces initial output and revisions given critique feedback |
| **Critic** | Evaluates output against an explicit rubric; returns pass/fail + structured feedback |
| **Iteration Guard** | Enforces a maximum iteration count to prevent infinite loops |
| **Dead Letter Agent** | Receives escalations when the loop exhausts its iteration budget without passing |

---

## Consequences

**Benefits:**
- ✅ Output quality improves measurably over single-pass generation on complex, criteria-bound tasks
- ✅ Explicit rubric makes quality objective and auditable — not "did it feel right?" but "did it satisfy criterion X?"
- ✅ Critique feedback is loggable; failure patterns reveal which criteria are hard and which prompts help
- ✅ Loop terminates safely when iteration guard is properly wired

**Trade-offs:**
- ❌ Each revision cycle adds latency (F1) and token cost (F3); budget per task must be accounted for
- ❌ A Generator and Critic that share the same base model share blind spots — correlated errors survive the loop
- ❌ Rubric design is non-trivial; poorly specified criteria push the complexity into prompt engineering
- ❌ Loop cadence must match task complexity — tight loops for structured tasks, slower deliberate loops for synthesis; mismatch produces shallow revisions or frustrating delays

---

## Implementation

```python
from dataclasses import dataclass

@dataclass
class LoopResult:
    output: str
    passed: bool
    iterations: int

def reflection_loop(
    task: str,
    rubric: list[str],
    generator,
    critic,
    max_iterations: int = 5,
) -> LoopResult:
    draft = generator.generate(task)
    for i in range(1, max_iterations + 1):
        verdict = critic.evaluate(draft, rubric)
        if verdict.passed:
            return LoopResult(output=draft, passed=True, iterations=i)
        draft = generator.generate(task, critique=verdict.feedback)
    return LoopResult(output=draft, passed=False, iterations=max_iterations)
```

---

## Known Uses

- **LangGraph LCEL** — `RunnableWithFallbacks` + self-critique chains; LangChain Self-Critique Chain.
- **AutoGen** — `ConversableAgent` critic patterns in AutoGen's built-in two-agent reflection examples.
- **Anthropic Cookbook** — "Constitutional AI" as a Generate → Critique → Revise loop at scale.
- **MindStudio Harness Engineering** — Critic-Generator Loop identified as a primary harness pattern (2025).
- **Madaan et al. (2023)** — "Self-Refine: Iterative Refinement with Self-Feedback" (NeurIPS 2023) — foundational empirical work showing multi-round self-critique improves quality across diverse tasks.

---

## Related Patterns

- [LLM-as-Judge](llm-as-judge.md) — single-pass evaluation; Reflection Loop uses LLM-as-Judge as its Critic but adds the revision cycle.
- [Ensemble Judge](ensemble-judge.md) — use Ensemble Judge as the Critic when the exit condition requires high-confidence verdicts.
- [Dead Letter Agent](../resilience/dead-letter-agent.md) — escalation target when the loop exhausts its iteration budget.
- [Checkpoint & Resume](../resilience/checkpoint-resume.md) — persist the best draft across iterations so a crash does not restart from zero.
- [Circuit Breaker](../resilience/circuit-breaker.md) — open the breaker if the Critic is systematically unavailable to avoid burning the iteration budget.

---

## Failure Modes Mitigated

Maps to MAST (Cemri et al. 2025, arXiv:2503.13657):

| MAST Failure Mode | How Reflection Loop mitigates it |
|---|---|
| FM-2.6 Reasoning–action mismatch | Critic catches mismatches between stated reasoning and produced output before delivery |
| FM-1.1 Disobey task specification | Rubric encodes the specification; Critic rejects output that violates it |
| FM-3.1 Premature termination | Loop continues until rubric criteria are met, not until the Generator decides it is done |
| FM-3.2 No or incomplete verification | Every iteration produces a Critic verdict — verification is structural, not optional |

**Primary MAST alignment:** FM-2.6 (Reasoning–action mismatch) — the loop's core mechanism is catching the gap between what the agent *intended* and what it *produced*.

---

## References

- Madaan, A. et al. (2023). *Self-Refine: Iterative Refinement with Self-Feedback.* NeurIPS 2023.
- MindStudio. (2025). *Loop Engineering vs Harness Engineering.* mindstudio.ai/blog.
- MindStudio. (2025). *What is Harness Engineering?* mindstudio.ai/blog.
- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* MAST. arXiv:2503.13657.
- Shinn, N. et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning.* NeurIPS 2023.
