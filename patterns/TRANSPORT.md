# Transport Considerations

*How the physical transport layer shapes agent integration pattern selection and behavior.*

The patterns in this catalog are transport-agnostic by design — they describe *what* agents do, not *how* bytes move. But transport choice is not implementation detail: it determines achievable latency, connection lifecycle, streaming capability, reconnection behavior, and blast radius when links fail. This document maps transports to patterns and calls out the interactions that matter.

---

## Transport overview

| Transport | Protocol | Directionality | Streaming | Persistence | Best for |
|-----------|----------|----------------|-----------|-------------|----------|
| **stdio** | pipe | bidirectional | yes (line-by-line) | no | local MCP servers, subprocess agents |
| **HTTP/1.1** | TCP | request/response | SSE (server→client) | no | A2A task delegation, MCP remote |
| **HTTP/2** | TCP (TLS) | multiplexed | yes (streams) | no | parallel tool calls, low-latency A2A |
| **HTTP/3 / QUIC** | UDP | multiplexed | yes (streams) | no | edge agents, unstable networks |
| **WebSocket** | TCP (upgrade) | bidirectional | yes | no | interactive agents, real-time feedback |
| **gRPC** | HTTP/2 | bidirectional | yes (streaming RPC) | no | typed agent APIs, service meshes |
| **NATS / JetStream** | TCP | pub/sub | JetStream replay | JetStream | broadcast, ephemeral agent events |
| **Apache Kafka** | TCP | pub/sub | yes (offsets) | yes (log) | high-throughput pipelines, audit trails |
| **Apache Iggy** | TCP / HTTP / QUIC | pub/sub | yes | yes (log) | low-latency streaming, QUIC-native |
| **RabbitMQ (AMQP)** | TCP | pub/sub + routing | no | optional | routed delivery, dead-letter queues |
| **Redis Streams** | TCP | pub/sub | yes (XREAD) | yes (in-memory) | lightweight pipelines, fast fanout |

---

## How the two agent protocols map to transports

### Model Context Protocol (MCP)

MCP (Anthropic, v2025-11-25) defines two official transports:

- **stdio** — agent and MCP server run as sibling processes; frames are newline-delimited JSON-RPC. Zero network overhead; the default for local tool servers (Claude Desktop, Claude Code).
- **HTTP + SSE** — agent connects to a remote MCP server over HTTPS. The initial handshake is HTTP POST; long-running or streamed results come back as Server-Sent Events on the same connection.

**HTTP/2 impact on MCP:** When an agent issues multiple tool calls in parallel (Tool Provider fanout), HTTP/1.1 opens one TCP connection per call. HTTP/2 multiplexes all calls onto one connection — no head-of-line blocking between requests. For high-fanout patterns (Scatter-Gather, Ensemble Judge each calling a tool), HTTP/2 cuts connection setup overhead and saturates available bandwidth instead of serializing calls.

**HTTP/3 / QUIC impact on MCP:** QUIC's 0-RTT handshake eliminates the TCP+TLS round-trips on reconnection. For agents on unstable links (mobile, edge, serverless with cold starts), this reduces the Circuit Breaker's open→half-open recovery time. QUIC also delivers connection migration — an agent's IP can change mid-session without dropping the MCP stream.

### Agent-to-Agent (A2A)

A2A (Google, April 2025) is built on HTTP/1.1+ with JSON bodies. Task streaming uses SSE: the orchestrator receives incremental `TaskStatusUpdateEvent` objects as the remote agent works.

**HTTP/2 multiplexing for A2A:** An Orchestrator delegating to N workers opens N parallel A2A requests. Over HTTP/1.1, each is a separate TCP connection (or queued on a keep-alive). Over HTTP/2, all N streams share one connection to the same host — relevant when multiple workers run behind a shared gateway or load balancer.

**gRPC as A2A transport:** gRPC (HTTP/2-based) is not part of the A2A spec but is common in internal agent meshes. It adds strong typing via Protobuf and bidirectional streaming. The Orchestrator → Worker relationship maps cleanly to a gRPC streaming RPC where the worker sends progress updates and a final result.

---

## Pattern-to-transport mapping

### Messaging Patterns

| Pattern | Recommended transport(s) | Notes |
|---------|--------------------------|-------|
| **Direct Message** | HTTP/2, gRPC, A2A over HTTP | Use HTTP/2 for low latency; gRPC for typed contracts in internal meshes |
| **Broadcast Message** | NATS, Kafka, Redis Streams, Iggy | Pub/sub brokers decouple publisher from subscriber count; SSE for browser-facing agents |
| **Blackboard** | Redis Streams, Kafka (compacted topic) | Persistent log gives Checkpoint & Resume a replay source; Redis for in-memory speed |

### Discovery Patterns

| Pattern | Recommended transport(s) | Notes |
|---------|--------------------------|-------|
| **Agent Card Registry** | HTTP/1.1+ (A2A spec), HTTP/2 for bulk discovery | Agent Cards served at `/.well-known/agent.json`; polling or push-on-change via SSE |
| **Agent Proxy** | HTTP/2, gRPC | Proxy benefits most from HTTP/2 multiplexing — it fans in multiple upstream connections |
| **Broker** | HTTP/2, NATS JetStream | Broker routes to capability providers; NATS JetStream for ephemeral task queues |

### Context Patterns

| Pattern | Recommended transport(s) | Notes |
|---------|--------------------------|-------|
| **Context Injection** | MCP stdio, MCP HTTP+SSE | MCP Resources are the canonical transport for injected context |
| **Tool Provider** | MCP stdio (local), MCP HTTP/2 (remote) | HTTP/2 multiplexing is significant when multiple tools are called concurrently |

### Routing Patterns

| Pattern | Recommended transport(s) | Notes |
|---------|--------------------------|-------|
| **Pipeline** | Kafka, Iggy, gRPC streaming | Each stage writes to a topic/stream; next stage consumes; natural backpressure |
| **Scatter-Gather** | HTTP/2 (parallel requests), NATS | Scatter over HTTP/2 avoids connection per worker; gather via response streams |
| **Content-Based Router** | NATS subject routing, Kafka topic routing | Route by subject/topic key rather than by LLM decision for deterministic paths |

### Coordination Patterns

| Pattern | Recommended transport(s) | Notes |
|---------|--------------------------|-------|
| **Orchestrator** | A2A over HTTP/2, gRPC bidirectional | Bidirectional streaming lets workers push progress without polling |
| **Choreography** | Kafka, NATS, Iggy | Event-driven choreography is a natural fit for persistent log transports |
| **Saga / Compensating Action** | Kafka (transactional), RabbitMQ (dead-letter) | Saga steps need durable delivery; compensating actions often routed via dead-letter |
| **Mediator Agent** | NATS, RabbitMQ | Mediator receives all messages on one queue; routes responses back on reply-to queues |

### Resilience Patterns

| Pattern | Recommended transport(s) | Notes |
|---------|--------------------------|-------|
| **Circuit Breaker** | HTTP/2, gRPC | HTTP/2 stream reset (RST_STREAM) is a clean half-open probe; gRPC adds health checks |
| **Checkpoint & Resume** | Kafka (offset commit), Redis Streams (XACK) | The transport offset *is* the checkpoint — no separate persistence needed |
| **Dead Letter Agent** | RabbitMQ (x-dead-letter-exchange), Kafka DLQ topic | RabbitMQ's native DLX routes undeliverable messages; Kafka uses a separate DLQ topic |
| **Idempotent Agent** | any | Transport-agnostic; idempotency key lives in message headers |

### Security Patterns

| Pattern | Recommended transport(s) | Notes |
|---------|--------------------------|-------|
| **Trust Boundary** | mTLS over HTTP/2, QUIC with client certs | QUIC 0-RTT requires careful replay protection when used with trust tiers |
| **Least-Privilege Tool Scope** | MCP (scope enforced at server) | Transport-agnostic; scope enforced at the MCP server layer |
| **Prompt Firewall** | any, inline filter | Firewall sits between the transport ingestion point and agent context |

### Evaluation Patterns

| Pattern | Recommended transport(s) | Notes |
|---------|--------------------------|-------|
| **LLM-as-Judge** | HTTP/2, A2A | Judge is a standard agent call; HTTP/2 avoids blocking if called alongside producer |
| **Ensemble Judge** | HTTP/2 parallel, gRPC streaming | Fan-out to N judges benefits from HTTP/2 multiplexing or gRPC bidirectional streams |
| **Reflection Loop** | HTTP/2, gRPC streaming | Each iteration is a round-trip; HTTP/2 keeps connection alive across iterations |

---

## Streaming transports in depth

### Apache Iggy

[Apache Iggy](https://iggy.apache.org) is a persistent message streaming platform written in Rust. It exposes three transports natively:

- **TCP** — binary protocol, lowest latency
- **HTTP** — REST-compatible, firewall-friendly
- **QUIC** — multiplexed, 0-RTT, connection migration

**Agent integration fit:**
- **Choreography** — Iggy topics replace Kafka topics with lower operational overhead for small-to-medium deployments
- **Pipeline** — Iggy's consumer groups provide natural backpressure between pipeline stages
- **Checkpoint & Resume** — Iggy stream offsets serve as checkpoints; replay from any offset on restart
- **Broadcast Message** — Iggy's QUIC transport makes broadcast to geographically distributed agents viable without Kafka's operational complexity

**Versus Kafka:** Iggy's QUIC transport eliminates TCP head-of-line blocking on lossy links; Kafka wins on ecosystem maturity and exactly-once semantics. Choose Iggy for latency-sensitive, QUIC-native deployments; Kafka for audit-critical, high-throughput pipelines.

### NATS / JetStream

[NATS](https://nats.io) is a lightweight pub/sub with JetStream for persistence.

- **Core NATS** (no persistence): excellent for ephemeral agent events (tool-call results, heartbeats)
- **JetStream** (persistence + replay): suitable for Choreography and Checkpoint & Resume
- **Request-Reply** pattern: maps directly to Direct Message with timeout semantics built into the protocol

### Kafka

[Apache Kafka](https://kafka.apache.org) is the default for high-throughput, ordered, replayable pipelines.

- **Exactly-once semantics** (EOS): required for Saga / Compensating Action to avoid double-application of compensating steps
- **Log compaction**: use for Blackboard topics — only the latest value per key is retained, giving a snapshot of shared state
- **Dead Letter Topics**: route undeliverable or repeatedly-failed messages to a `_dlq` topic consumed by Dead Letter Agent

### RabbitMQ

[RabbitMQ](https://rabbitmq.com) (AMQP 0-9-1 / 1.0) adds routing semantics that map to agentic patterns:

- **Dead Letter Exchange (DLX)**: native dead-lettering for messages that are rejected, expired, or queue-length-exceeded — the cleanest fit for Dead Letter Agent
- **Topic Exchange**: route tasks to workers by routing key — maps to Content-Based Router
- **Competing consumers** on a single queue: load balancing across Orchestrator workers

---

## HTTP/2 and HTTP/3 in practice

### HTTP/2 quick-reference for agent systems

| Feature | Agent benefit |
|---------|--------------|
| **Stream multiplexing** | N parallel tool calls or worker delegations over one TCP connection |
| **Header compression (HPACK)** | Reduces overhead for repetitive MCP/A2A headers (Content-Type, Authorization) |
| **Server Push** | Not widely used in agent protocols today; SSE serves the same push need |
| **Connection reuse** | Orchestrators maintain a single long-lived connection per worker host |

Enable HTTP/2 at the load balancer (e.g., nginx `listen 443 http2`, Envoy `http2_protocol_options`) and ensure the MCP or A2A server speaks h2 — most modern frameworks (FastAPI + hypercorn, Spring Boot 3.x, Go `net/http`) support it with minimal config.

### HTTP/3 / QUIC quick-reference for agent systems

| Feature | Agent benefit |
|---------|--------------|
| **0-RTT handshake** | Cold-start reconnection after Circuit Breaker half-open in ~0ms vs. ~3× TCP+TLS RTT |
| **No head-of-line blocking** | Loss of one UDP datagram does not stall unrelated agent streams |
| **Connection migration** | Agent IP change (mobile, serverless) does not drop an in-flight MCP session |
| **Stateless retry** | QUIC retry tokens are replay-resistant — safe for Idempotent Agent patterns |

QUIC is most impactful for **edge-deployed agents** (CDN workers, IoT gateway agents, mobile-hosted agents) where TCP's connection establishment cost and HOL blocking are felt acutely. For datacenter-to-datacenter agent communication, HTTP/2 over a stable TCP connection is typically sufficient.

**Iggy's QUIC transport** makes it the only streaming platform in this catalog that exposes QUIC natively — without a reverse proxy in front.

---

## Selecting a transport

```
Is the agent local (same process or machine)?
  └─ YES → stdio (MCP), in-process queue
  └─ NO  →
       Is the message persistent / replayable?
         └─ YES → Kafka (high throughput/audit), Iggy (QUIC-native), RabbitMQ (routing), Redis Streams (light)
         └─ NO  →
              Is the connection long-lived or bidirectional?
                └─ YES → WebSocket, gRPC bidirectional, NATS
                └─ NO  →
                     Is network reliability a concern (edge, mobile)?
                       └─ YES → HTTP/3 / QUIC (Iggy QUIC, QUIC-aware proxy)
                       └─ NO  → HTTP/2 (default for A2A, MCP remote, gRPC)
```

---

## Force interactions

Transport choice directly engages two forces from the shared force catalog:

- **F14 Transport latency / reliability** — protocol stack (HTTP/2 vs. HTTP/3 vs. message broker) determines baseline latency, reconnection cost, and HOL blocking exposure.
- **F1 Latency** — transport overhead is the floor; pattern overhead (retries, fan-out hops) adds above it.
- **F8 Determinism** — brokers with exactly-once semantics (Kafka EOS, RabbitMQ publisher confirms) are required for deterministic Saga execution and idempotent checkpointing.
- **F5 Blast radius** — mTLS + QUIC client certificates shrink the blast radius of a compromised connection; bare TCP has no mutual authentication at the transport layer.

See [`FORCES.md`](FORCES.md) for the full force catalog.

---

## References

- Anthropic. (2025). *Model Context Protocol Specification v2025-11-25.* modelcontextprotocol.io.
- Google. (2025). *Agent-to-Agent (A2A) Protocol Specification.* a2a-protocol.org.
- IETF. (2022). *RFC 9114 — HTTP/3.* datatracker.ietf.org/doc/rfc9114.
- IETF. (2021). *RFC 9000 — QUIC: A UDP-Based Multiplexed and Secure Transport.* datatracker.ietf.org/doc/rfc9000.
- IETF. (2015). *RFC 7540 — Hypertext Transfer Protocol Version 2 (HTTP/2).*
- Apache Iggy. (2025). *Iggy Documentation.* iggy.apache.org.
- NATS.io. (2025). *NATS JetStream Documentation.* docs.nats.io.
- Apache Kafka. (2025). *Kafka Documentation.* kafka.apache.org.
- RabbitMQ. (2025). *RabbitMQ Documentation.* rabbitmq.com.
- MindStudio. (2025). *What is Harness Engineering?* mindstudio.ai/blog.
