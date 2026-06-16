# Least-Privilege Tool Scope

> Grant each agent access only to the minimum set of tools and resources required for its task.

**Category:** Security
**Maturity:** ★ Emerging
**Also known as:** Scoped Tool Access, Tool ACL, Minimal Capability, Tool Allowlist
**EIP Analog:** No direct EIP analog — applies the security principle of least privilege to the MCP tool layer

---

## Intent

Grant each agent access only to the minimum set of tools and resources required for its task. Tool scope is enforced at the MCP server level, not by prompting the agent to self-restrict.

---

## Context

Multi-agent systems connect agents to powerful tools: code execution, database writes, file deletion, external API calls. When every agent shares the same tool surface, any failure — prompt injection, LLM error, or misconfigured prompt — carries the same blast radius as the most powerful tool in the set.

---

## Problem

Agents with access to powerful tools can cause irreversible damage through prompt injection attacks, LLM errors, or misconfigured prompts. Giving every agent access to all tools amplifies the blast radius of any failure and makes security audits impractical because no single agent's capability surface is bounded or inspectable.

---

## Forces

- **F5 Blast radius vs. F10 Adaptability** — the core tension: scoping tools limits what a compromised or misbehaving agent can do (F5), but also limits what a legitimate agent can accomplish dynamically (F10).
- **F7 Trust asymmetry** — different agents warrant different tool access; a research agent should not have write access regardless of what it asks for.
- **F11 Operational complexity** — maintaining per-agent tool allowlists adds configuration overhead; allowlists must be updated when agent roles evolve.

---

## Solution

Define tool scopes at the MCP server level. Each agent role receives a connection to an MCP server configured with only the tools and resources relevant to that role. Scope is enforced by the MCP server — not by prompting the agent to "only use certain tools." An agent that cannot see a tool cannot call it.

---

## Diagram

![Least-Privilege Tool Scope — Research Agent connects via MCP to read-only server (search_web, read_document); Execution Agent connects via MCP to write-scope server (write_file, run_code)](../../img/least-privilege-tool-scope.png)

---

## Participants

| Participant | Role |
|---|---|
| **Agent** | Operates within its tool scope; cannot request tools outside its MCP server's exposure |
| **Scoped MCP Server** | Configured with a specific subset of tools for a specific agent role |
| **Tool Administrator** | Defines and maintains scope definitions per agent role |

---

## Sample Code

Runnable implementation: [samples/python/security/least_privilege_tool_scope.py](../../samples/python/security/least_privilege_tool_scope.py)

```python
# Scoped MCP server — only exposes read-only tools to the research agent
from mcp.server import Server
from mcp import types

# READ-ONLY scope for Research Agent
research_server = Server("research-tools")

@research_server.list_tools()
async def research_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_web",
            description="Search the web for information",
            inputSchema={"type": "object", "properties": {"query": {"type": "string"}}},
        ),
        types.Tool(
            name="read_document",
            description="Read a document by URL",
            inputSchema={"type": "object", "properties": {"url": {"type": "string"}}},
        ),
        # write_file, run_code, delete_* are NOT listed — agent cannot call them
    ]


# WRITE scope for Execution Agent — separate server instance
execution_server = Server("execution-tools")

@execution_server.list_tools()
async def execution_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="write_file",
            description="Write content to a file",
            inputSchema={
                "type": "object",
                "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
            },
        ),
        types.Tool(
            name="run_code",
            description="Execute Python code in a sandbox",
            inputSchema={"type": "object", "properties": {"code": {"type": "string"}}},
        ),
        # delete_database is NOT listed — even execution agents don't have this
    ]
```

---

## Consequences

- ✅ Limits blast radius on compromise (F5 resolved)
- ✅ Makes each agent's capability surface explicit and auditable
- ❌ Overly restrictive scopes slow legitimate work (F10 cost)
- ❌ Allowlist maintenance overhead (F11 introduced)

---

## When to Avoid

- When all agents are fully trusted and operate in a closed, isolated environment.
- When the overhead of per-agent allowlists exceeds the security benefit (low-risk internal tools).

---

## Failure Modes Mitigated

Per [FAILURE-MAP.md](../FAILURE-MAP.md):
Beyond MAST, this pattern is the primary defense against **privilege escalation** — an agent calling tools outside its intended role — and limits the damage from **prompt injection** attacks that try to use the agent as a proxy for destructive tool calls.

---

## Known Uses

- **Anthropic MCP permission model** — Claude Desktop and Claude.ai allow users to configure which MCP servers (and therefore which tools) each session can access
- **AWS IAM roles for agents** — each AWS Bedrock agent assumes an IAM role with only the permissions needed for its tasks
- **Anthropic's guidance on minimal footprint** — explicitly recommends requesting only necessary permissions and preferring reversible over irreversible actions

---

## Related Patterns

- *complements* [Trust Boundary](trust-boundary.md) — Trust Boundary controls *who* can call; Least-Privilege controls *what* they can do once trusted.
- *complements* [Prompt Firewall](prompt-firewall.md) — firewall sanitizes inputs; least-privilege limits outputs (tool calls).
- *used-by* [Tool Provider](../context/tool-provider.md) — the tool provider implements the allowlist enforcement.

---

## References

- OWASP (2025). *LLM Top 10* — LLM06: Excessive Agency.
- *From Glue-Code to Protocols: A Critical Analysis of A2A and MCP Security.* arXiv:2505.03864.
- Cemri, M. et al. (2025). arXiv:2503.13657.
- [Anthropic: Building Effective Agents — Minimal Footprint](https://www.anthropic.com/research/building-effective-agents)
