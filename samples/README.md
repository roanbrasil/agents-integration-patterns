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
