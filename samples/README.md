# Samples

Runnable code samples for all 22 Agent Integration Patterns.

## Structure

```
samples/
  python/               # Python samples — LangChain / LangGraph
    messaging/ discovery/ context/ routing/ coordination/ resilience/ security/ evaluation/
    requirements.txt
  java/                 # Java samples — Spring AI 1.0.0 + Mockito tests
    pom.xml
    src/main/java/com/agents/patterns/<category>/
    src/test/java/com/agents/patterns/<category>/
  typescript/           # TypeScript samples — LangChain.js / LangGraph.js
    messaging/ discovery/ context/ routing/ coordination/ resilience/ security/ evaluation/
    package.json  tsconfig.json
  csharp/               # C# samples — Microsoft Semantic Kernel
    src/AgentPatterns/<category>/
    tests/AgentPatterns.Tests/<category>/
    AgentPatterns.sln
```

## Python

**Requirements:** Python 3.10+, `ANTHROPIC_API_KEY` set.

```bash
cd samples/python
pip install -r requirements.txt

# Run tests (no API key needed — uses mocks)
python3 -m pytest tests/ -v    # 63 tests, all patterns covered

# Run samples against real API
export ANTHROPIC_API_KEY=your-key-here
python3 messaging/direct_message.py
python3 routing/pipeline.py
python3 evaluation/ensemble_judge.py
```

All samples use `claude-haiku-4-5-20251001` for fast, low-cost execution.

| Category | File | Pattern |
|---|---|---|
| messaging | `direct_message.py` | Direct Message |
| messaging | `broadcast_message.py` | Broadcast Message |
| messaging | `blackboard.py` | Blackboard |
| discovery | `agent_card_registry.py` | Agent Card Registry |
| discovery | `agent_proxy.py` | Agent Proxy |
| context | `context_injection.py` | Context Injection |
| context | `tool_provider.py` | Tool Provider |
| routing | `content_based_router.py` | Content-Based Router |
| routing | `scatter_gather.py` | Scatter-Gather |
| routing | `pipeline.py` | Pipeline |
| coordination | `supervised_delegation.py` | Supervised Delegation |
| coordination | `orchestrator.py` | Orchestrator |
| coordination | `choreography.py` | Choreography |
| coordination | `peer_to_peer_delegation.py` | Peer-to-Peer Delegation |
| resilience | `dead_letter_agent.py` | Dead Letter Agent |
| resilience | `circuit_breaker.py` | Circuit Breaker |
| resilience | `checkpoint_resume.py` | Checkpoint & Resume |
| security | `least_privilege_tool_scope.py` | Least-Privilege Tool Scope |
| security | `trust_boundary.py` | Trust Boundary |
| security | `prompt_firewall.py` | Prompt Firewall |
| evaluation | `llm_as_judge.py` | LLM-as-Judge |
| evaluation | `ensemble_judge.py` | Ensemble Judge |

## Java (Spring AI)

**Requirements:** Java 21+, Maven 3.6+. Tests use Mockito — no API key needed.

```bash
cd samples/java
mvn test        # compile + run all 32 Mockito tests (no API key required)
```

To run against a real Anthropic API, set the key in `application.properties`:
```properties
spring.ai.anthropic.api-key=your-key-here
```

| Category | Implementation | Test |
|---|---|---|
| messaging | `DirectMessage.java` | `DirectMessageTest.java` |
| messaging | `BroadcastMessage.java` | `BroadcastMessageTest.java` |
| messaging | `Blackboard.java` | `BlackboardTest.java` |
| discovery | `AgentCardRegistry.java` | `AgentCardRegistryTest.java` |
| discovery | `AgentProxy.java` | `AgentProxyTest.java` |
| context | `ContextInjection.java` | `ContextInjectionTest.java` |
| context | `ToolProvider.java` | `ToolProviderTest.java` |
| routing | `ContentBasedRouter.java` | `ContentBasedRouterTest.java` |
| routing | `ScatterGather.java` | `ScatterGatherTest.java` |
| routing | `Pipeline.java` | `PipelineTest.java` |
| coordination | `SupervisedDelegation.java` | `SupervisedDelegationTest.java` |
| coordination | `Orchestrator.java` | `OrchestratorTest.java` |
| coordination | `Choreography.java` | `ChoreographyTest.java` |
| coordination | `PeerToPeerDelegation.java` | `PeerToPeerDelegationTest.java` |
| resilience | `DeadLetterAgent.java` | `DeadLetterAgentTest.java` |
| resilience | `CircuitBreaker.java` | `CircuitBreakerTest.java` |
| resilience | `CheckpointResume.java` | `CheckpointResumeTest.java` |
| security | `LeastPrivilegeToolScope.java` | `LeastPrivilegeToolScopeTest.java` |
| security | `TrustBoundary.java` | `TrustBoundaryTest.java` |
| security | `PromptFirewall.java` | `PromptFirewallTest.java` |
| evaluation | `LlmAsJudge.java` | `LlmAsJudgeTest.java` |
| evaluation | `EnsembleJudge.java` | `EnsembleJudgeTest.java` |

## TypeScript (LangChain.js / LangGraph.js)

**Requirements:** Node.js 18+, `ANTHROPIC_API_KEY` set.

```bash
cd samples/typescript
npm install
export ANTHROPIC_API_KEY=your-key-here

# Run any pattern
npx tsx messaging/direct_message.ts
npx tsx routing/pipeline.ts
npx tsx evaluation/ensemble_judge.ts

# Type-check all 22 files (no API key needed)
npx tsc --noEmit
```

All samples use `claude-haiku-4-5-20251001`.

| Category | File | Pattern |
|---|---|---|
| messaging | `direct_message.ts` | Direct Message |
| messaging | `broadcast_message.ts` | Broadcast Message |
| messaging | `blackboard.ts` | Blackboard |
| discovery | `agent_card_registry.ts` | Agent Card Registry |
| discovery | `agent_proxy.ts` | Agent Proxy |
| context | `context_injection.ts` | Context Injection |
| context | `tool_provider.ts` | Tool Provider |
| routing | `content_based_router.ts` | Content-Based Router |
| routing | `scatter_gather.ts` | Scatter-Gather |
| routing | `pipeline.ts` | Pipeline |
| coordination | `supervised_delegation.ts` | Supervised Delegation |
| coordination | `orchestrator.ts` | Orchestrator |
| coordination | `choreography.ts` | Choreography |
| coordination | `peer_to_peer_delegation.ts` | Peer-to-Peer Delegation |
| resilience | `dead_letter_agent.ts` | Dead Letter Agent |
| resilience | `circuit_breaker.ts` | Circuit Breaker |
| resilience | `checkpoint_resume.ts` | Checkpoint & Resume |
| security | `least_privilege_tool_scope.ts` | Least-Privilege Tool Scope |
| security | `trust_boundary.ts` | Trust Boundary |
| security | `prompt_firewall.ts` | Prompt Firewall |
| evaluation | `llm_as_judge.ts` | LLM-as-Judge |
| evaluation | `ensemble_judge.ts` | Ensemble Judge |

## C# (Microsoft Semantic Kernel)

**Requirements:** .NET 9 SDK. Tests use Moq — no API key needed.

```bash
cd samples/csharp
dotnet test        # compile + run all 34 tests (no API key required)
```

To run a specific pattern against a real Anthropic API, set the key in your environment:
```bash
export ANTHROPIC_API_KEY=your-key-here
```

| Category | Implementation | Test |
|---|---|---|
| messaging | `Messaging/DirectMessage.cs` | `Messaging/DirectMessageTests.cs` |
| messaging | `Messaging/BroadcastMessage.cs` | `Messaging/BroadcastMessageTests.cs` |
| messaging | `Messaging/Blackboard.cs` | `Messaging/BlackboardTests.cs` |
| discovery | `Discovery/AgentCardRegistry.cs` | `Discovery/AgentCardRegistryTests.cs` |
| discovery | `Discovery/AgentProxy.cs` | `Discovery/AgentProxyTests.cs` |
| context | `Context/ContextInjection.cs` | `Context/ContextInjectionTests.cs` |
| context | `Context/ToolProvider.cs` | `Context/ToolProviderTests.cs` |
| routing | `Routing/ContentBasedRouter.cs` | `Routing/ContentBasedRouterTests.cs` |
| routing | `Routing/ScatterGather.cs` | `Routing/ScatterGatherTests.cs` |
| routing | `Routing/Pipeline.cs` | `Routing/PipelineTests.cs` |
| coordination | `Coordination/SupervisedDelegation.cs` | `Coordination/SupervisedDelegationTests.cs` |
| coordination | `Coordination/Orchestrator.cs` | `Coordination/OrchestratorTests.cs` |
| coordination | `Coordination/Choreography.cs` | `Coordination/ChoreographyTests.cs` |
| coordination | `Coordination/PeerToPeerDelegation.cs` | `Coordination/PeerToPeerDelegationTests.cs` |
| resilience | `Resilience/DeadLetterAgent.cs` | `Resilience/DeadLetterAgentTests.cs` |
| resilience | `Resilience/CircuitBreaker.cs` | `Resilience/CircuitBreakerTests.cs` |
| resilience | `Resilience/CheckpointResume.cs` | `Resilience/CheckpointResumeTests.cs` |
| security | `Security/LeastPrivilegeToolScope.cs` | `Security/LeastPrivilegeToolScopeTests.cs` |
| security | `Security/TrustBoundary.cs` | `Security/TrustBoundaryTests.cs` |
| security | `Security/PromptFirewall.cs` | `Security/PromptFirewallTests.cs` |
| evaluation | `Evaluation/LlmAsJudge.cs` | `Evaluation/LlmAsJudgeTests.cs` |
| evaluation | `Evaluation/EnsembleJudge.cs` | `Evaluation/EnsembleJudgeTests.cs` |

## Rust

**Requirements:** Rust 1.75+ (2021 edition), Cargo. No API key needed — all examples use a deterministic `FakeAgent`.

```bash
cd samples/rust

# Check all examples compile
cargo check

# Run any pattern
cargo run --example messaging_direct_message
cargo run --example routing_pipeline
cargo run --example resilience_circuit_breaker
cargo run --example evaluation_reflection_loop
# etc.
```

All examples run fully offline. Each is a self-contained `examples/<category>_<pattern>.rs` file using `FakeAgent` from `src/lib.rs`.

| Category | Example | Pattern |
|---|---|---|
| messaging | `messaging_direct_message` | Direct Message |
| messaging | `messaging_broadcast_message` | Broadcast Message |
| messaging | `messaging_blackboard` | Blackboard |
| discovery | `discovery_agent_card_registry` | Agent Card Registry |
| discovery | `discovery_agent_proxy` | Agent Proxy |
| discovery | `discovery_broker` | Broker |
| context | `context_context_injection` | Context Injection |
| context | `context_tool_provider` | Tool Provider |
| routing | `routing_content_based_router` | Content-Based Router |
| routing | `routing_scatter_gather` | Scatter-Gather |
| routing | `routing_pipeline` | Pipeline |
| coordination | `coordination_orchestrator` | Orchestrator |
| coordination | `coordination_supervised_delegation` | Supervised Delegation |
| coordination | `coordination_choreography` | Choreography |
| coordination | `coordination_peer_to_peer_delegation` | Peer-to-Peer Delegation |
| coordination | `coordination_mediator` | Mediator Agent |
| coordination | `coordination_group_chat` | Group Chat |
| coordination | `coordination_saga` | Saga / Compensating Action |
| coordination | `coordination_magentic` | Magentic |
| resilience | `resilience_circuit_breaker` | Circuit Breaker |
| resilience | `resilience_dead_letter_agent` | Dead Letter Agent |
| resilience | `resilience_checkpoint_resume` | Checkpoint & Resume |
| implementation | `implementation_idempotent_agent` | Idempotent Agent |
| security | `security_least_privilege_tool_scope` | Least-Privilege Tool Scope |
| security | `security_trust_boundary` | Trust Boundary |
| security | `security_prompt_firewall` | Prompt Firewall |
| evaluation | `evaluation_llm_as_judge` | LLM-as-Judge |
| evaluation | `evaluation_ensemble_judge` | Ensemble Judge |
| evaluation | `evaluation_reflection_loop` | Reflection Loop |

## Go

**Requirements:** Go 1.22+. No API key needed — all patterns use a deterministic `FakeAgent` from `shared/fake_agent.go`. No external dependencies (stdlib only).

```bash
cd samples/go

# Run all patterns at once
go run ./cmd/main.go

# Run a single pattern file directly
go run ./messaging/direct_message.go ./shared/fake_agent.go

# Build check
go build ./...
```

Each pattern file exposes a `Run()` function. `cmd/main.go` calls all 29 of them in sequence.

| Category | File | Pattern |
|---|---|---|
| messaging | `messaging/direct_message.go` | Direct Message |
| messaging | `messaging/broadcast_message.go` | Broadcast Message |
| messaging | `messaging/blackboard.go` | Blackboard |
| discovery | `discovery/agent_card_registry.go` | Agent Card Registry |
| discovery | `discovery/agent_proxy.go` | Agent Proxy |
| discovery | `discovery/broker.go` | Broker |
| context | `context/context_injection.go` | Context Injection |
| context | `context/tool_provider.go` | Tool Provider |
| routing | `routing/content_based_router.go` | Content-Based Router |
| routing | `routing/scatter_gather.go` | Scatter-Gather |
| routing | `routing/pipeline.go` | Pipeline |
| coordination | `coordination/orchestrator.go` | Orchestrator |
| coordination | `coordination/supervised_delegation.go` | Supervised Delegation |
| coordination | `coordination/choreography.go` | Choreography |
| coordination | `coordination/peer_to_peer_delegation.go` | Peer-to-Peer Delegation |
| coordination | `coordination/mediator.go` | Mediator Agent |
| coordination | `coordination/group_chat.go` | Group Chat |
| coordination | `coordination/saga.go` | Saga / Compensating Action |
| coordination | `coordination/magentic.go` | Magentic |
| resilience | `resilience/circuit_breaker.go` | Circuit Breaker |
| resilience | `resilience/dead_letter_agent.go` | Dead Letter Agent |
| resilience | `resilience/checkpoint_resume.go` | Checkpoint & Resume |
| implementation | `implementation/idempotent_agent.go` | Idempotent Agent |
| security | `security/least_privilege_tool_scope.go` | Least-Privilege Tool Scope |
| security | `security/trust_boundary.go` | Trust Boundary |
| security | `security/prompt_firewall.go` | Prompt Firewall |
| evaluation | `evaluation/llm_as_judge.go` | LLM-as-Judge |
| evaluation | `evaluation/ensemble_judge.go` | Ensemble Judge |
| evaluation | `evaluation/reflection_loop.go` | Reflection Loop |
