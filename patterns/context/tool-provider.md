# Tool Provider

> Expose capabilities as invocable tools through a standardized interface, decoupling agents from specific implementations.

**Category:** context
**EIP Analog:** No direct EIP analog — closest is [Service Activator](https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessagingAdapter.html)

---

## Also Known As

MCP Tool Server, Function Provider, Skill Endpoint

---

## Problem

Agents need to take actions in the world: query databases, call APIs, execute code, search the web, write files. Hardcoding these capabilities into agents makes them brittle, non-reusable, and hard to test. Different agents may need the same capability — duplicating the implementation is wasteful and inconsistent.

---

## Solution

Wrap capabilities as MCP Tools with structured input/output schemas. Agents discover available tools via `tools/list` and invoke them via `tools/call`. The Tool Provider handles execution and returns structured results. Agents remain unaware of implementation details — they only know the tool's name and schema.

---

## Diagram

![Tool Provider — Agent interacts with MCP Tool Server through a stateful Context State layer carrying JSON/TEXT, session_id, and memory](../../img/tool-provider.png)

> **Note:** The diagram illustrates the stateful session model — the Context State layer (session_id, JSON/TEXT, memory) represents the MCP client's internal session object that tracks tool schema discovery and call state across turns. In stateless or single-turn invocations, the Agent calls `tools/list` and `tools/call` directly against the MCP Tool Server without a persistent Context State.

---

## Participants

| Participant | Role |
|---|---|
| **Agent (MCP Client)** | Discovers and invokes tools; treats them as black boxes |
| **MCP Tool Server** | Hosts tool implementations; exposes `tools/list` and `tools/call` endpoints |
| **Tools** | Individual capability implementations (functions, API wrappers, scripts) |

---

## Consequences

**Benefits:**
- ✅ Agents are completely decoupled from tool implementations
- ✅ Tools can be versioned, replaced, or mocked independently of agents
- ✅ Any MCP-compatible agent can use any MCP tool server — framework agnostic

**Trade-offs:**
- ❌ Tool schemas must be carefully designed; poor descriptions and schemas confuse LLMs
- ❌ Tool explosion — too many tools in `tools/list` degrades agent performance and decision-making
- ❌ Tool calls add round-trip latency compared to in-process function calls

---

## Implementation

```python
# MCP Tool Server exposing web search and code execution
from mcp.server import Server
from mcp import types
import subprocess, httpx

app = Server("capability-server")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_web",
            description="Search the web and return top results as text",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string", "description": "Search query"}},
                "required": ["query"],
            },
        ),
        types.Tool(
            name="run_python",
            description="Execute Python code in a sandbox and return stdout",
            inputSchema={
                "type": "object",
                "properties": {"code": {"type": "string", "description": "Python code to run"}},
                "required": ["code"],
            },
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "search_web":
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://api.search.example.com/search",
                params={"q": arguments["query"]},
            )
            return [types.TextContent(type="text", text=resp.json()["results"][0]["text"])]

    if name == "run_python":
        result = subprocess.run(
            ["python", "-c", arguments["code"]],
            capture_output=True, text=True, timeout=10
        )
        return [types.TextContent(type="text", text=result.stdout)]
```

---

## Known Uses

- **Claude Desktop / Claude.ai** — MCP tool servers expose file system, databases, and APIs as tools that Claude invokes during conversation
- **LangChain Tools** — the LangChain `@tool` decorator and `StructuredTool` follow the same interface pattern as MCP tools
- **OpenAI Function Calling** — the original popularization of structured tool invocation by LLMs; MCP generalizes this across providers

---

## Related Patterns

- [Context Injection](./context-injection.md) — use instead when agents need read-only context assembled before reasoning, not active tool invocation
- [Least-Privilege Tool Scope](../security/least-privilege-tool-scope.md) — limit which tools each agent can see and call
- [Circuit Breaker](../resilience/circuit-breaker.md) — protect agents from failing tool servers

---

## References

- [MCP Tools Specification](https://modelcontextprotocol.io/docs/concepts/tools)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
