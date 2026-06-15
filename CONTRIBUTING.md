# Contributing to Agents Integration Patterns

Thank you for helping build the shared vocabulary for multi-agent AI systems.

---

## What belongs here

This catalog follows the same principle as Enterprise Integration Patterns: **named, reusable solutions to recurring integration problems**. A contribution belongs here if it describes:

- A structural solution to a recurring problem when integrating AI agents, tools, or models
- A pattern that appears in more than one system or framework (not a one-off design)
- Something prescriptive: intent + problem + solution + trade-offs (not just an observation)

**Does not belong here:**
- Framework tutorials or how-to guides
- Architecture documentation for a specific product
- Patterns about internal agent behavior (planning, memory management) — those are agent design patterns, not integration patterns

---

## Pattern categories

| Category | What it covers |
|---|---|
| `messaging/` | How agents exchange information |
| `discovery/` | How agents find each other |
| `context/` | How agents share and manage contextual information |
| `routing/` | How tasks are distributed across agents |
| `coordination/` | How agents decide who does what |
| `resilience/` | How agent systems fail gracefully and recover |
| `security/` | How to establish trust and limit blast radius |

If your pattern doesn't fit any existing category, propose a new one in your issue first.

---

## How to propose a new pattern

1. **Open an issue** using the [Pattern Proposal template](.github/ISSUE_TEMPLATE/pattern-proposal.md)
2. Include: name, one-sentence intent, the problem it solves, and at least one known use in a real system
3. Wait for community feedback before writing the full pattern file (saves work if the idea needs refinement)

---

## How to write a pattern

Use [`patterns/_template.md`](patterns/_template.md) as your starting point.

Every pattern must have:

| Field | Required | Notes |
|---|---|---|
| **Name** | ✅ | Noun phrase describing the structural role (e.g., "Dead Letter Agent", not "Handle Failures") |
| **Also Known As** | — | Other names used in frameworks or papers |
| **Intent** | ✅ | One sentence. What this pattern does. |
| **Problem** | ✅ | What forces this resolves. Must be specific. |
| **Solution** | ✅ | The structural approach. |
| **Diagram** | ✅ | ASCII or Mermaid diagram in the file |
| **Participants** | ✅ | Who/what plays each role |
| **Consequences** | ✅ | At least 2 benefits and 2 trade-offs |
| **Implementation** | ✅ | Working code snippet (Python preferred; LangGraph/MCP/A2A when applicable) |
| **Known Uses** | ✅ | At least 2 real systems (framework, product, or paper) |
| **Related Patterns** | ✅ | Links to patterns in this catalog |
| **EIP Analog** | — | Closest Enterprise Integration Pattern, or "No direct analog" with explanation |

---

## Submitting a pull request

1. Fork the repository
2. Create a branch: `pattern/<pattern-name>` or `fix/<what-you-fixed>`
3. Write or edit the pattern file following the template
4. Update the relevant category `README.md` to include your pattern in the table
5. If adding an EN pattern, consider adding the PT translation under `patterns/pt/`
6. Open a PR with:
   - Title: `[Pattern] Pattern Name` or `[Fix] What you fixed`
   - Description: why this pattern belongs here and where you've seen it used

---

## Reviewing patterns

Reviews focus on:
- **Recurrence**: Is this a recurring problem, not a one-off?
- **Prescriptiveness**: Does the solution give enough structure to implement?
- **Trade-offs**: Are the consequences honest? Patterns have costs.
- **Known uses**: Is this observed in real systems, not invented?

---

## Updating existing patterns

Patterns evolve as protocols and frameworks mature. Good updates include:
- Adding a new known use in a production system
- Updating a code example to reflect a new framework version
- Adding an implementation in a new language/framework
- Correcting a consequence that turned out to be wrong

---

## Translations

We maintain parallel EN and PT versions. If you translate a pattern:
- Place it in `patterns/pt/<category>/<pattern-name>.md`
- Keep the structure and code examples identical; translate prose and comments
- Update the PT catalog index

Other languages are welcome — open an issue to discuss adding a new language directory.

---

## License

By contributing, you agree that your contributions will be licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
