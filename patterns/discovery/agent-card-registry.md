# Agent Card Registry

> Allow agents to advertise their capabilities and be discovered by other agents at runtime without prior configuration.

**Category:** discovery
**EIP Analog:** No direct EIP analog — closest is Service Registry (SOA/microservices)

---

## Also Known As

Capability Registry, Agent Marketplace, Agent Discovery Service

---

## Problem

In a dynamic multi-agent system, you cannot hardcode which agent handles which task. New agents join, capabilities change, and agents may be versioned or temporarily unavailable. Routing decisions must happen at runtime based on current, live capability information — not static configuration.

---

## Solution

Each agent publishes an **Agent Card** — a structured capability manifest — at a well-known endpoint (`/.well-known/agent.json`). A registry indexes these cards. When an agent or orchestrator needs a capability, it queries the registry and receives a list of agents that can fulfill the request, along with their endpoints and authentication requirements.

---

## Diagram

```
Agent Card (served at /.well-known/agent.json):
{
  "name": "DataExtractionAgent",
  "description": "Extracts structured data from PDFs and images",
  "skills": [
    { "id": "pdf-extract", "name": "PDF Text Extraction" },
    { "id": "img-ocr",    "name": "Image OCR" }
  ],
  "url": "https://agents.example.com/extractor",
  "authentication": { "schemes": ["bearer"] }
}

 ┌──────────┐  "who has pdf-extract?"  ┌──────────────────┐
 │ Agent A  │ ─────────────────────── ►│  Agent Registry  │
 │          │ ◄──────────────────────  │  (Agent Cards)   │
 └──────────┘  "Agent B @ url + token" └──────────────────┘
      │
      │ establishes A2A channel
      ▼
 ┌──────────┐
 │ Agent B  │
 └──────────┘
```

---

## Participants

| Participant | Role |
|---|---|
| **Agent** | Publishes its Agent Card at a well-known URL; keeps it updated |
| **Registry** | Indexes Agent Cards; answers capability queries |
| **Consumer Agent** | Queries the registry for needed capabilities; connects directly to the discovered agent |

---

## Consequences

**Benefits:**
- ✅ Dynamic composition — agents join and leave without global reconfiguration
- ✅ Capability-based routing — consumers find agents by what they can do, not by name
- ✅ Enables multi-framework interoperability (LangGraph agents discoverable by AutoGen agents)

**Trade-offs:**
- ❌ Registry becomes a single point of failure; requires high availability
- ❌ Stale cards if agents fail without deregistering
- ❌ Trust verification of discovered agents requires additional security layers

---

## Implementation

```python
# Serving an Agent Card (A2A spec)
from fastapi import FastAPI
from a2a.types import AgentCard, AgentSkill, AgentCapabilities

app = FastAPI()

AGENT_CARD = AgentCard(
    name="ResearchAgent",
    description="Searches the web and synthesizes information on any topic",
    url="https://agents.example.com/research",
    version="1.0.0",
    skills=[
        AgentSkill(
            id="web-research",
            name="Web Research",
            description="Search and synthesize information from the web",
            inputModes=["text"],
            outputModes=["text"],
        )
    ],
    capabilities=AgentCapabilities(streaming=True),
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
)

@app.get("/.well-known/agent.json")
async def get_agent_card():
    return AGENT_CARD.model_dump(exclude_none=True)


# Discovering agents (consumer side)
import httpx

async def find_agent_with_skill(registry_url: str, skill_id: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{registry_url}/agents?skill={skill_id}")
        agents = resp.json()
        return agents[0]["url"]  # return first matching agent's URL
```

---

## Known Uses

- **Google A2A Protocol** — defines the Agent Card schema and `/.well-known/agent.json` convention as the standard discovery mechanism
- **AWS Bedrock Agent Aliases** — agents are registered with capability metadata and discovered by orchestration layers
- **Azure AI Foundry** — agent catalog provides capability-based discovery across deployed agent resources

---

## Related Patterns

- [Agent Proxy](./agent-proxy.md) — use to present a stable interface after discovery
- [Content-Based Router](../routing/content-based-router.md) — use Agent Card data to route tasks at the orchestrator level
- [Direct Message](../messaging/direct-message.md) — the communication pattern used after discovery

---

## References

- [A2A Agent Card Specification](https://a2a-protocol.org/specification/latest/Agent-to-Agent%20Protocol%20Specification#agent-card)
- Google Developer Blog: [A2A: A New Era of Agent Interoperability](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
