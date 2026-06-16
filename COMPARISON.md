# How This Catalog Relates to Other Work

*Where Agents Integration Patterns sits among the existing vocabularies — and what gap it fills.*

Several excellent resources describe agent patterns. They serve different purposes and overlap only partially. This page maps the landscape honestly: what each source does well, and why a dedicated *integration* catalog is still needed.

---

## At a glance

| Source | Scope | Structure | Empirical grounding | Lineage to EIP |
|--------|-------|-----------|--------------------|----------------|
| **This catalog** | 7 categories: messaging, discovery, context, routing, coordination, resilience, security, evaluation | Full pattern template (Intent → **Forces** → Solution → Consequences → **Failure modes** → Known uses → Related) | Patterns mapped to MAST failure modes | Systematic, explicit mapping table |
| **Microsoft — Azure Architecture Center** | Coordination only: 5 orchestration patterns | "Intent + when to use / when to avoid + example" | "Proven approaches"; no failure data | Mentioned in passing ("resembles Pipes and Filters") |
| **Anthropic — Building Effective Agents** | Workflows vs. agents; ~5 building blocks | Prose + diagrams, principle-driven | Practitioner experience | None |
| **LangChain/LangGraph docs** | Multi-agent architectures (supervisor, swarm, network) | Framework-specific how-to | Usage-driven | None |
| **12-Factor Agents (HumanLayer)** | Operational principles (12 factors) | Numbered principles | Practitioner experience | Borrowed framing from 12-factor apps |
| **Academic surveys** (arXiv:2501.06322, 2502.14321, 2506.05364) | Taxonomies of communication/collaboration | Descriptive dimensions | Literature synthesis | Re-evaluates classical GoF patterns |
| **Enterprise Integration Patterns** (Hohpe & Woolf, 2003) | 65 messaging patterns | The canonical pattern template | 20 years of middleware practice | *is* the origin |

---

## Microsoft — AI Agent Orchestration Patterns

The closest peer, and the most directly comparable. Microsoft's catalog is prescriptive, technology-agnostic, and production-grounded. Its five patterns map cleanly onto this catalog:

| Microsoft pattern | This catalog |
|---|---|
| Sequential (pipeline, prompt chaining) | **Pipeline** |
| Concurrent (fan-out/fan-in, scatter-gather, map-reduce) | **Scatter-Gather** |
| Group Chat (roundtable, debate, council) | **Group Chat** |
| Handoff (routing, triage, dispatch) | **Content-Based Router** + **Peer-to-Peer Delegation** |
| Magentic (dynamic task ledger) | **Magentic** |
| Maker-Checker (sub-pattern) | **Group Chat** (turn-based variant) / **Reflection Loop** |

**What Microsoft does better, and this catalog adopts:**

- **The complexity-ladder.** Microsoft opens by asking *do you even need multiagent?* (direct model call → single agent with tools → multiagent). That honesty belongs at the front of any agent catalog. See the README's "Do you need this?" section, credited to them.
- **Crisp "when to avoid" lists.** Fast decision triggers an architect reads first. This catalog now includes a **When to avoid** section per pattern.
- **Aggressive "also known as."** Microsoft lists synonyms generously — exactly the vocabulary-unification work this catalog exists to do.

**What this catalog adds beyond Microsoft:**

- **Six more categories.** Microsoft covers coordination only. Security, resilience, discovery, context, and evaluation have no equivalent there — yet these are where the MAST data says production systems actually break.
- **Empirical failure grounding.** Microsoft says "proven"; this catalog says *which of the 14 MAST failure modes each pattern mitigates*, with a citation.
- **Named forces.** Microsoft has prose "considerations"; this catalog has a referenceable force vocabulary (F1–F11).
- **EIP lineage.** Microsoft mentions it in passing; this catalog maps every pattern to its 2003 ancestor (or marks it genuinely new).

---

## Anthropic — Building Effective Agents

A principles piece, not a catalog. Its enduring contribution is the **workflows vs. agents** distinction and a handful of building blocks (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer). This catalog cites it as a known use for **Pipeline**, **Content-Based Router**, **Scatter-Gather**, **Orchestrator**, and **Group Chat / Reflection**. Anthropic tells you *when to reach for agents at all*; this catalog tells you *how to wire them together once you do*.

---

## LangChain / LangGraph

Framework documentation, not a framework-agnostic catalog. Its supervisor / swarm / network taxonomy maps to **Supervised Delegation**, **Peer-to-Peer Delegation**, and **Choreography**. LangGraph is cited throughout as a known use (StateGraph → Orchestrator, checkpointers → Checkpoint & Resume). The difference: this catalog names patterns independently of any one framework, so the vocabulary survives a framework migration.

---

## 12-Factor Agents

Operational principles ("own your control flow," "own your context window"), not integration patterns. Complementary, not overlapping: 12-factor tells you how to *build a reliable agent*; this catalog tells you how to *connect agents to each other and to tools*. Cited as a known use for **Checkpoint & Resume**.

---

## Academic surveys

The surveys (multi-agent collaboration mechanisms, communication-centric reviews, the MCP design-pattern review) are *descriptive taxonomies* — they classify the space along dimensions. They are invaluable as grounding and this catalog cites them throughout, but they stop short of *prescriptive, named patterns* with intent/forces/solution/consequences. The MCP-centric review (arXiv:2506.05364) is the bridge: it re-evaluates classical GoF patterns (Mediator, Observer, Broker) for agents — directly supporting this catalog's **Mediator** and **Broker** entries.

---

## The gap this catalog fills

No existing resource combines all five of:

1. **Breadth** — integration across all seven concern categories, not coordination alone.
2. **Prescriptive structure** — the full Alexander/GoF/Hohpe template, including **Forces**.
3. **Empirical grounding** — patterns tied to the MAST failure taxonomy.
4. **Framework neutrality** — vocabulary that outlives any one SDK.
5. **Explicit EIP lineage** — continuity with two decades of integration practice.

Microsoft has (2) and partial (4); Anthropic has principle-level (2); the surveys have (3) descriptively; EIP has (2) and (5) but predates agents. **The combination is the contribution** — the aim is to be the *Enterprise Integration Patterns* of the agentic era, not to replace any of the above.

---

## References

- Microsoft (2026). *AI Agent Orchestration Patterns.* Azure Architecture Center.
- Anthropic (2024). *Building Effective Agents.*
- LangChain. *Multi-agent architectures.* LangGraph documentation.
- HumanLayer (2025). *12-Factor Agents.*
- Sarkar, A. & Sarkar, S. (2025). *Survey of LLM Agent Communication with MCP.* arXiv:2506.05364.
- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv:2503.13657.
- Hohpe, G. & Woolf, B. (2003). *Enterprise Integration Patterns.*
