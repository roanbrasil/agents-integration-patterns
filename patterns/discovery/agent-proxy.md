# Agent Proxy

**Category:** Discovery
**Maturity:** ★★ Established
**Also known as:** Gateway Agent, Protocol Adapter, Agent Façade

> Provide a stable interface to an agent (or group of agents) while hiding implementation details, protocol differences, or versioning.

**EIP Analog:** [Messaging Gateway](https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessagingGateway.html)

---

## Intent

Introduce a proxy agent that presents a uniform interface to consumers, hiding whether the backend is a single LLM call, a sub-graph of agents, an external API, or a different protocol. The proxy centralises cross-cutting concerns — authentication, rate limiting, protocol translation, and versioning — so that neither the consumer nor the backend need to carry that complexity.

---

## Context

Multi-agent systems frequently need to integrate agents built with different frameworks (LangGraph, AutoGen, CrewAI), exposed over different protocols (A2A, MCP, REST), or owned by different teams with independent release cycles. Without a stable façade, every consumer must negotiate the address, protocol, and authentication scheme of every backend agent directly.

---

## Problem

Consumers of an agent's capabilities should not need to know whether the agent is a single LLM call, a sub-graph of agents, an external API, or which protocol it speaks. Exposing implementation details forces consumers to change when the implementation changes. You also need a single place to handle versioning, load balancing, authentication, and protocol translation.

---

## Forces

- **F2 Coupling** — the proxy is the indirection layer; callers do not depend on the backend agent's address, protocol, or authentication scheme.
- **F7 Trust asymmetry** — the proxy is the single enforcement point for auth, rate limiting, and input sanitization before the backend agent is reached.
- **F1 Latency** — every call adds one hop; acceptable when the benefits (protocol translation, retry, auth) justify it.
- **F4 Reliability** — the proxy can add retry logic and circuit-breaker behavior that the caller does not need to implement.

---

## Solution

Introduce a proxy agent that presents a uniform interface. The proxy translates protocols (e.g., A2A ↔ MCP), routes to appropriate backend agents, manages versioning, and handles cross-cutting concerns like authentication and rate limiting. Consumers interact only with the proxy.

---

## Diagram

![Agent Proxy — Client Agent sends request to Agent Proxy, which authenticates, transforms, and forwards to the remote Agent B](../../img/agent-proxy.png)

### Participants

| Participant | Role |
|---|---|
| **Consumer Agent** | Uses the proxy as if it were the real agent; protocol-agnostic |
| **Proxy** | Presents a uniform interface; handles translation, auth, routing, and versioning |
| **Backend(s)** | The real agent(s) or tool(s) that do the actual work |

---

## Sample Code

Runnable implementation: [samples/python/discovery/agent_proxy.py](../../samples/python/discovery/agent_proxy.py)

```python
# MCP proxy server that wraps an A2A agent as an MCP tool
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp import types
from a2a.client import A2AClient

app = Server("agent-proxy")
a2a_client = A2AClient(url="https://agents.example.com/research")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="research",
            description="Search and synthesize information on any topic",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "research":
        # Translate MCP tool call → A2A task request
        result = await a2a_client.send_task_and_wait(
            message=arguments["query"]
        )
        return [types.TextContent(type="text", text=result.text)]
```

---

## Consequences

**Benefits:**
- Decouples consumers from implementation — swap backends without touching consumers.
- Single place for cross-cutting concerns: auth, logging, rate limiting, circuit breaking.
- Enables A/B testing and gradual migration between agent versions.

**Trade-offs:**
- Adds a network hop and latency.
- The proxy itself becomes a bottleneck if it holds state.
- Protocol translation is complex and can introduce subtle semantic mismatches.

---

## When to Avoid

- When you control both caller and backend and no protocol translation is needed — direct calls are simpler.
- When the proxy becomes a bottleneck under load — consider horizontal scaling or removing it.

---

## Failure Modes Mitigated

Per [FAILURE-MAP.md](../FAILURE-MAP.md):

- **FM-2.3 Task derailment** (partial) — the proxy validates and sanitizes inputs before forwarding, reducing injection-driven derailment (overlaps with Trust Boundary).
- **FM-3.1 Premature termination** (partial) — retry logic in the proxy prevents transient failures from terminating the task prematurely.

---

## Known Uses

- **LangGraph remote agent nodes** — LangGraph can expose a sub-graph as a remote agent endpoint, acting as a proxy to a complex internal workflow.
- **MCP proxy servers** — proxy servers that aggregate multiple MCP tool servers behind a single endpoint.
- **API gateways for agent endpoints** — cloud-hosted gateways (AWS API Gateway, Azure APIM) acting as proxies to agent services.

---

## Related Patterns

- *uses* [Agent Card Registry](agent-card-registry.md) — the proxy discovers the backend via the registry.
- *complements* [Trust Boundary](../security/trust-boundary.md) — the proxy is often the gateway tier implementation.
- *complements* [Circuit Breaker](../resilience/circuit-breaker.md) — proxy + circuit breaker = a robust remote agent façade.

---

## References

- Hohpe, G. & Woolf, B. (2003). *Enterprise Integration Patterns* — Message Endpoint, Gateway.
- *From Glue-Code to Protocols: A Critical Analysis of A2A and MCP Security.* arXiv:2505.03864.
- [MCP Proxy Servers](https://modelcontextprotocol.io/docs/concepts/architecture)
