# Engineering Roadmap — `agents-integration-patterns`

*A plan to evolve the repository from a strong README into a rigorous, citable, executable pattern language.*

---

## Guiding principles

Three findings from the literature shape this entire roadmap:

1. **Patterns need Forces, not just Problem/Solution.** The canonical GoF/Alexander template is *Name → Problem → **Forces** → Solution → Consequences → Known Uses → Related Patterns* (Gamma et al. 1994; Alexander et al. 1977; extended to integration by Hohpe & Woolf 2003). The current catalog collapses Forces into Consequences. Forces are what make a pattern *generative* — they capture the competing tensions (latency vs. coupling, cost vs. reliability) that justify the trade-off. This is the single highest-leverage structural fix.

2. **A pattern catalog earns authority by being grounded in empirical failure data.** MAST — the Multi-Agent System Failure Taxonomy (Cemri et al., NeurIPS 2025, arXiv:2503.13657) — analyzed 1,600+ execution traces across 7 frameworks and found 41–86.7% failure rates, clustering 14 failure modes into three categories: (i) specification & system design, (ii) inter-agent misalignment, (iii) task verification & termination. Critically, they conclude that *better base models will not fix these failures — they are system-design problems*. **No existing pattern catalog maps patterns to the failure modes they mitigate.** That is the repository's strongest possible differentiator.

3. **A catalog becomes a *language* only when patterns are interlinked and rated for maturity.** Alexander rated each pattern with 0–2 stars by how well it was proven in the real world. A pattern language (vs. a loose catalog) requires explicit, typed relationships between patterns (Stuttgart IAAS, 2018) and honest maturity signaling — which protects readers from treating a speculative pattern as battle-tested.

Every work item below traces back to one of these three principles.

---

## Track 1 — Reference code (`samples/`)

**Goal:** Every one of the 22 patterns has a runnable, tested, minimal implementation. This is what separates a blog-post catalog from an engineering reference.

### Structure

```
samples/
├── README.md                      # how to run, dependency matrix, pattern→sample index
├── pyproject.toml                 # single installable package: `aip-samples`
├── shared/
│   ├── fake_agent.py              # deterministic stub agent (no API key needed for tests)
│   ├── fake_mcp_server.py         # in-memory MCP server for tests
│   └── tracing.py                 # OpenTelemetry span helpers (see Track 5)
├── messaging/
│   ├── direct_message/
│   │   ├── pattern.py             # the implementation
│   │   ├── example.py             # runnable demo with __main__
│   │   ├── test_pattern.py        # pytest, runs against fake_agent (no network)
│   │   └── README.md             # links back to patterns/messaging/direct-message.md
│   ├── broadcast_message/
│   └── blackboard/
├── discovery/ … routing/ … coordination/ … resilience/ … security/ … evaluation/
```

### Engineering standards (non-negotiable)

- **Two-tier testing.** Every sample runs against a *deterministic fake* (no API key, runs in CI) AND has an optional live integration test gated behind an env var (`AIP_LIVE=1`). The fake is what makes the catalog trustworthy — a contributor on any machine can prove the pattern works.
- **No hidden state.** Each `pattern.py` exposes one clear entry function/class with typed signatures. The pattern *is* the interface, not the framework glue around it.
- **Framework-honest.** Where a pattern is idiomatic to a framework (Pipeline → LangGraph, Tool Provider → FastMCP), show the framework version. Where it is framework-agnostic (Circuit Breaker, Blackboard), show plain Python so the *pattern* is visible, not the library.
- **Each sample is < 120 lines.** If it grows past that, the pattern is leaking implementation detail. Samples teach the shape, not a production system.

### Why this ordering is first

Code is the proof. A reader skeptical of "Ensemble Judge" can run `python -m aip_samples.evaluation.ensemble_judge.example` and watch three judges disagree. Nothing else in the roadmap builds trust faster.

---

## Track 2 — Diagrams (`img/`)

**Goal:** Replace ad-hoc PNGs with a consistent, regenerable, accessible SVG set in the series' retro-terminal aesthetic.

### Approach

- **Diagrams as code, not hand-drawn.** Author each diagram in a text source (Mermaid for flow/sequence, or hand-written SVG templates for the brand look) committed alongside the PNG/SVG output. This makes diagrams reviewable in PRs and regenerable when a pattern changes.
- **One visual grammar across all 22.** Fixed conventions: agents are rounded rectangles, channels are solid arrows, events are dashed arrows, trust boundaries are dotted enclosures, data stores are cylinders. A reader who learns the grammar once reads every diagram instantly. This consistency *is* the language.
- **Accessibility.** Every diagram needs a real `alt`/`<title>`/`<desc>` describing the flow (the current README alt-text is good — formalize it). SVG also means it scales and stays crisp in dark mode.
- **A single legend diagram** at the top of the README defining the visual grammar, so the conventions are explicit rather than inferred.

### Build step

A `make diagrams` target (or a small `scripts/render_diagrams.py`) that turns every `*.mmd` / `*.svg.j2` source into final assets, so diagrams never drift from their source.

---

## Track 3 — Expanded pattern files (`patterns/`)

**Goal:** Turn each `patterns/**/<name>.md` from a README echo into the authoritative, citable pattern document. **This is where Principles 1 and 2 land.**

### New canonical template (apply to all 22)

```markdown
# <Pattern Name>

**Category:** Messaging | Discovery | … 
**Maturity:** ★★ Established | ★ Emerging | ☆ Proposed     ← Alexandrian star rating
**Also known as:** <aliases teams use — collects the synonyms this catalog unifies>

## Intent
One sentence.

## Context
When you are already in this situation (the precondition that makes the pattern relevant).

## Problem
The recurring problem, stated independently of any solution.

## Forces                                       ← NEW, the key addition
The competing tensions the pattern must balance, e.g.:
- Latency pulls toward direct calls; resilience pulls toward an intermediary.
- Token cost pulls toward a single agent; answer quality pulls toward an ensemble.
(Forces are what make the pattern a *decision*, not a recipe.)

## Solution
Structural approach. Prose + the canonical diagram.

## Sample Code
Link to the runnable sample in `samples/…` (Track 1). Short inline excerpt only.

## Consequences
✅ Forces resolved.  ❌ Forces introduced / new liabilities.

## Failure Modes Mitigated                       ← NEW, the differentiator
Maps to MAST (Cemri et al. 2025) and SHIELDA where applicable, e.g.:
- Mitigates MAST FM-2.4 "Information withholding" (inter-agent misalignment).
- Mitigates MAST FM-3.1 "Premature termination" (task verification).
This is what no other agent catalog does.

## Known Uses
Production systems / frameworks, with links. Demote vague claims to "reported in."

## Related Patterns
Typed links: *uses* / *used-by* / *alternative-to* / *refines* / *conflicts-with*.
(Typed relationships are what make this a language, not a list.)

## References
Numbered, real citations only.
```

### Two new cross-cutting documents

- **`patterns/FORCES.md`** — a catalog of the recurring forces themselves (latency, coupling, token cost, blast radius, observability, trust asymmetry, determinism). Each pattern references shared forces. This is the connective tissue Alexander calls a pattern language.
- **`patterns/FAILURE-MAP.md`** — a matrix: 14 MAST failure modes × 22 patterns, showing which pattern mitigates which failure. This single table is the most defensible, most citable, most novel artifact the repo can publish.

---

## Track 4 — New patterns

**Goal:** Close the gaps the literature and your own "What Comes Next" identified — but only add a pattern when there is a real recurring problem and at least one known use (Alexander's bar: no pattern without real-world examples).

### High-confidence additions (have known uses today)

| Pattern | Category | Problem it solves | Grounding |
|---|---|---|---|
| **Idempotent Agent** | Resilience | Resume/retry produces duplicates; non-idempotent tool calls corrupt state | Pairs with Checkpoint & Resume; 12-factor "own your control flow" |
| **Saga / Compensating Action** | Coordination | A multi-agent workflow partially completes then fails; needs rollback | EIP Saga; agent-based saga (already cited in Choreography) |
| **Exception Handler Chain** | Resilience | Unstructured error handling is a top MAST failure cause | SHIELDA, arXiv:2508.07935 — structured exception handling for agentic workflows |
| **Mediator Agent** | Coordination | N agents create N² direct couplings; need centralized interaction | Sarkar & Sarkar survey (arXiv:2506.05364) maps Mediator → supervisor LLM |
| **Broker** | Discovery | Dynamic match of task to capability provider at runtime | MCP broker pattern; classical Broker (Buschmann POSA) |

### Emerging (mark ☆ Proposed until known uses solidify)

- **Rate-Limited Tool Scope** (Security) — cost/abuse control as a first-class scope dimension
- **Multi-modal Context Injection** (Context) — vision/audio as MCP resources
- **Reflection Loop** (Evaluation) — self-critique before external judging
- **Token-Budget Governor** (Resilience) — bounded spend per task, ties to your token-efficiency research

### Discipline

Each new pattern must ship with: the expanded template (Track 3), a runnable sample (Track 1), and a diagram (Track 2). **No orphan patterns.** A pattern without code and a known use is a blog idea, not a catalog entry — keep those in a `DRAFTS.md`, not the catalog.

---

## Track 5 — CI / quality gates (GitHub Actions)

**Goal:** Make correctness mechanical. A pattern catalog that ships broken examples loses authority instantly.

### Workflows

- **`test.yml`** — run all `samples/**/test_*.py` against fakes on every PR (Python 3.11/3.12 matrix). Green check = every documented pattern provably runs.
- **`lint.yml`** — `ruff` + `mypy --strict` on `samples/`. Typed signatures are part of the teaching.
- **`docs.yml`** — a custom `scripts/validate_catalog.py` that asserts catalog integrity:
  - every pattern in README has a matching `patterns/**/*.md`
  - every pattern file has all required template sections (fails CI if `Forces` or `Failure Modes Mitigated` is missing)
  - every `Related Patterns` link resolves to an existing pattern (no dangling references)
  - every sample referenced by a pattern file exists
- **`diagrams.yml`** — regenerate diagrams from source and fail if committed output is stale.
- **`links.yml`** — scheduled (weekly) external link checker; known-uses links rot fast.

### Payoff

The custom catalog validator is itself a *demonstration of the Evaluation patterns* — it is an automated quality gate (LLM-as-Judge's deterministic cousin) applied to the repo's own content. That reflexivity is worth calling out in the README.

---

## Track 6 — Catalog site (GitHub Pages)

**Goal:** A navigable site, the way `enterpriseintegrationpatterns.com` is for EIP — but for agents.

### Approach

- **Generated from the `patterns/` files, not hand-maintained.** The expanded markdown (Track 3) is the single source of truth; the site is a view over it. Docusaurus or MkDocs Material both do this cleanly. This guarantees the site never contradicts the repo.
- **Three primary navigation axes**, because different readers arrive differently:
  1. **By category** (the 7 buckets) — for browsing
  2. **By failure mode** (the MAST map) — "I have *this* failure, which pattern helps?" — the killer entry point
  3. **By relationship graph** — an interactive view of the typed pattern links (the language made visible)
- **Per-pattern pages** render the full template, the diagram, and an embedded runnable snippet.
- **Stable URLs** (`/patterns/messaging/direct-message`) so the catalog is *citable* — patterns get referenced by URL the way EIP patterns are.

### Sequencing note

This is last because it is a *view*. It only pays off once Tracks 1–4 have produced real content and Track 5 guarantees that content is consistent. Building the site first would just be styling an empty shell.

---

## Suggested execution order

The tracks are numbered in dependency order, but here is the pragmatic sequence:

1. **Track 3 template + `FAILURE-MAP.md` for ~3 patterns** (one per top MAST category). Proves the new structure and the differentiator on a small slice before committing to all 22.
2. **Track 1 samples for those same 3 patterns**, with fakes and tests.
3. **Track 5 minimal CI** (`test.yml` + `validate_catalog.py`) so the structure is enforced from the start, not retrofitted.
4. **Roll Tracks 1+3 across all 22** patterns.
5. **Track 2 diagrams** in the unified grammar (can parallelize once the grammar legend is fixed).
6. **Track 4 new patterns**, each complete (code + doc + diagram).
7. **Track 6 site** as the capstone.

Doing one vertical slice end-to-end first (steps 1–3) de-risks the whole plan: you find the template's rough edges on 3 patterns, not 22.

---

## What this turns the repository into

A loose catalog answers *"what patterns exist?"* A pattern **language** answers *"I am in this situation, facing this failure — what do I reach for, and what does it cost me?"* The combination of **Forces** (why it's a decision), the **MAST failure map** (empirical grounding), **runnable tested samples** (proof), **typed relationships** (the language), and **honest maturity ratings** (trust) is what moves this repo from "nice README" to the reference work for agent integration — the *Enterprise Integration Patterns* of the agentic era.

---

## Key references

- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* MAST taxonomy. arXiv:2503.13657 (NeurIPS 2025 D&B).
- Sarkar, A. & Sarkar, S. (2025). *Survey of LLM Agent Communication with MCP: A Software Design Pattern Centric Review.* arXiv:2506.05364.
- *SHIELDA: Structured Handling of Exceptions in LLM-Driven Agentic Workflows.* arXiv:2508.07935.
- *A Survey of Agent Interoperability Protocols (MCP, ACP, A2A, ANP).* arXiv:2505.02279.
- Hohpe, G. & Woolf, B. (2003). *Enterprise Integration Patterns.*
- Gamma, E. et al. (1994). *Design Patterns* (GoF template).
- Alexander, C. et al. (1977). *A Pattern Language* (Forces, star ratings, generativity).
- Stuttgart IAAS (2018). *The Nature of Pattern Languages* (typed relationships).
