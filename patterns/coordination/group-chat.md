# Group Chat

**Category:** Coordination
**Maturity:** ★ Emerging
**Also known as:** Roundtable, Council, Multi-Agent Debate, Collaborative Discussion, Maker-Checker (turn-based variant)

## Intent

Let multiple agents solve a problem, make a decision, or validate work by participating in a shared conversation thread, coordinated by a chat manager that decides who speaks next.

## Context

You have a problem that benefits from *discussion* rather than hand-off or parallel fan-out — collaborative ideation, structured review, or consensus-building — and you can tolerate the latency of a multi-turn conversation. A human may want to observe or participate in real time.

## Problem

Some decisions are not reachable by a single agent or by independent parallel agents: they require agents to react to each other, challenge claims, and converge. A fixed pipeline cannot capture this, and a parallel scatter-gather discards the cross-talk that produces the insight.

## Forces

- **F4 Answer quality vs. F1 Latency / F3 Token cost** — discussion improves decisions but every turn re-sends the accumulating thread, so cost grows super-linearly with turns and participants.
- **F6 Observability** — a single accumulating thread is highly auditable (you can read exactly how the decision was reached)...
- **F6 vs. control** — ...but flow control gets harder as agents are added; loops and runaway threads are a real risk.

Group Chat spends latency and tokens (F1, F3) on quality and auditability (F4, F6). Microsoft's guidance: cap at **three or fewer agents** to keep flow controllable.

## Solution

A **chat manager** coordinates an accumulating conversation thread. It decides which agent responds next and manages the interaction mode — from free-flowing brainstorming to a formal turn-based review. Agents are typically **read-only** (they discuss; they do not call state-changing tools). A human can optionally take the chat-manager role or join as a participant.

The **Maker-Checker loop** is the structured, turn-based specialization: a *maker* proposes, a *checker* evaluates against acceptance criteria and either approves or returns specific feedback; the loop repeats under an iteration cap.

![Group Chat](../../img/group-chat.svg)

## Sample Code

Runnable, tested implementation: [`samples/coordination/group_chat/`](../../samples/coordination/group_chat/)

```python
# Excerpt — a chat manager drives a turn-based maker-checker loop
chat = GroupChat(manager=round_robin, max_turns=6)
chat.add("maker", maker_agent)
chat.add("checker", checker_agent)
result = chat.run("draft a refund policy")   # loops until checker approves or cap
```

## Consequences

- ✅ Captures cross-agent reasoning that pipelines and scatter-gather miss (resolves F4).
- ✅ Single accumulating thread is transparent and auditable; ideal for HITL (resolves F6).
- ❌ Token cost and latency grow with turns × participants (introduces F1, F3).
- ❌ Flow control degrades past ~3 agents; needs iteration caps and termination criteria.

## When to avoid

- A linear pipeline or simple delegation already suffices.
- Real-time latency budgets cannot absorb multi-turn discussion.
- The chat manager has **no objective way to decide the task is complete** — this is the classic infinite-loop trap.

## Failure Modes Mitigated

Per [FAILURE-MAP.md](../FAILURE-MAP.md):

- **FM-3.2 No or incomplete verification** ✅ — the maker-checker variant is a verification gate by construction.
- **FM-2.5 Ignored other agent's input** ✅ — the shared thread forces agents to read and respond to each other.
- **FM-2.6 Reasoning–action mismatch** ◐ — a checker catches outputs that do not follow from the discussion.
- **FM-3.1 Premature termination** ◐ — explicit acceptance criteria + iteration cap define a clean end.

## Known Uses

- **Microsoft Agent Framework** — *Group Chat* orchestration with a chat manager; *Maker-Checker* as the turn-based variant (Azure Architecture Center, 2026).
- Multi-agent debate (Google DeepMind).
- AutoGen `GroupChat` / `GroupChatManager`.

## Related Patterns

- *alternative-to* **[Scatter-Gather](../routing/scatter-gather.md)** — parallel, no cross-talk; choose it when independent perspectives suffice.
- *alternative-to* **[Blackboard](../messaging/blackboard.md)** — shared mutable *state* rather than a *conversation*; Group Chat is dialogue, Blackboard is a data store.
- *refines-into* **[Ensemble Judge](../evaluation/ensemble-judge.md)** — when "discussion" reduces to independent verdicts, prefer the cheaper parallel ensemble.
- *uses* **[Dead Letter Agent](../resilience/dead-letter-agent.md)** — escalation target when the iteration cap is hit without approval.

## References

- Microsoft (2026). *AI Agent Orchestration Patterns* — Group Chat & Maker-Checker. Azure Architecture Center.
- Du, Y. et al. (2023). *Improving Factuality and Reasoning via Multiagent Debate.*
- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv:2503.13657.
