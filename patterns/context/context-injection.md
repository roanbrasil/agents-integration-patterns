# Context Injection

> Supply an agent with relevant external context before it reasons, without the agent needing to fetch it.

**Category:** context
**EIP Analog:** [Content Enricher](https://www.enterpriseintegrationpatterns.com/patterns/messaging/DataEnricher.html)

---

## Also Known As

Retrieval-Augmented Generation (RAG), Context Assembly, Pre-fetching

---

## Problem

An agent's reasoning quality depends on context: documents, user history, database records, prior conversation. Requiring agents to actively fetch every piece of context they need is slow, couples them to specific data sources, and often exceeds context window limits. Agents should focus on reasoning, not retrieval.

---

## Solution

Before invoking an agent, a host or orchestrator retrieves relevant context from data sources (via MCP Resources or direct retrieval) and injects it into the agent's prompt or message. The agent receives pre-assembled context and focuses purely on reasoning over it.

---

## Diagram

```
 ┌───────────────────────────────────────────┐
 │                  Host                     │
 │                                           │
 │  User Query                               │
 │      │                                    │
 │      ▼                                    │
 │  ┌──────────┐     ┌─────────────────────┐ │
 │  │  MCP     │────►│  Context Assembler  │ │
 │  │ Resources│     │  (retrieve + rank)  │ │
 │  └──────────┘     └──────────┬──────────┘ │
 └─────────────────────────────┼─────────────┘
                                │ inject context into prompt
                                ▼
                          ┌──────────┐
                          │  Agent   │
                          │ (reason) │
                          └──────────┘
```

---

## Participants

| Participant | Role |
|---|---|
| **Host / Orchestrator** | Receives the query, retrieves context, assembles the enriched prompt |
| **Data Sources** | Databases, document stores, APIs accessed via MCP Resources or direct calls |
| **Context Assembler** | Retrieves, ranks, and formats context to fit within the agent's context window |
| **Agent** | Receives the enriched prompt; reasons over pre-assembled context |

---

## Consequences

**Benefits:**
- ✅ Agents stay stateless and focused on reasoning
- ✅ Context retrieval is controlled, auditable, and testable independently
- ✅ Same agent can work across different knowledge bases by changing the injected context

**Trade-offs:**
- ❌ Host must know what context is relevant — retrieval quality determines reasoning quality
- ❌ Large contexts consume tokens; retrieval must be precise to avoid noise
- ❌ Context can become stale if data sources change between injection and reasoning

---

## Implementation

```python
# RAG-style context injection using MCP Resources + LangChain
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

async def answer_with_context(query: str, mcp_client) -> str:
    # Step 1: retrieve relevant context via MCP
    resources = await mcp_client.read_resource(f"docs://search?q={query}")
    context_text = "\n\n".join(r.text for r in resources.contents)

    # Step 2: inject context into prompt before invoking agent
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer based only on the provided context.\n\nContext:\n{context}"),
        ("human", "{query}"),
    ])

    chain = prompt | ChatAnthropic(model="claude-sonnet-4-6")
    response = await chain.ainvoke({"context": context_text, "query": query})
    return response.content
```

---

## Known Uses

- **Anthropic Contextual Retrieval** — chunks documents with surrounding context before embedding, improving retrieval precision for injection
- **Claude Desktop with MCP Resources** — the host reads MCP resources and injects them into the context window before each Claude invocation
- **LangChain RAG chains** — the retriever runs before the LLM call; retrieved documents are formatted into the prompt

---

## Related Patterns

- [Tool Provider](./tool-provider.md) — use instead when agents need to actively query data during reasoning, not just at invocation time
- [Blackboard](../messaging/blackboard.md) — use instead when multiple agents need to read and write shared context across turns
- [Checkpoint & Resume](../resilience/checkpoint-resume.md) — inject checkpointed context to resume long-running tasks

---

## References

- [Anthropic: Contextual Retrieval](https://www.anthropic.com/research/contextual-retrieval)
- [MCP Resources Specification](https://modelcontextprotocol.io/docs/concepts/resources)
- Lewis et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." NeurIPS 2020.
