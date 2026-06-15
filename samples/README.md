# Samples

Runnable code samples for all 22 Agent Integration Patterns.

## Structure

```
samples/
  python/               # Python samples — LangChain / LangGraph
    messaging/
    discovery/
    context/
    routing/
    coordination/
    resilience/
    security/
    evaluation/
    requirements.txt
  java/                 # Java samples — Spring AI 1.0.0 + Mockito tests
    pom.xml
    src/main/java/com/agents/patterns/<category>/
    src/test/java/com/agents/patterns/<category>/
```

## Python

**Requirements:** Python 3.10+, `ANTHROPIC_API_KEY` set.

```bash
cd samples/python
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here

# Run any pattern
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
