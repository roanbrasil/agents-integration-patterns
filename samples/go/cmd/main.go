package main

import (
	"aip-samples/coordination"
	"aip-samples/context"
	"aip-samples/discovery"
	"aip-samples/evaluation"
	"aip-samples/implementation"
	"aip-samples/messaging"
	"aip-samples/resilience"
	"aip-samples/routing"
	"aip-samples/security"
	"fmt"
)

func sep() {
	fmt.Println("---")
}

func main() {
	fmt.Println("Agents Integration Patterns — Go Samples")
	fmt.Println("=========================================")
	fmt.Println()

	// Messaging
	messaging.RunDirectMessage()
	sep()
	messaging.RunBroadcastMessage()
	sep()
	messaging.RunBlackboard()
	sep()

	// Discovery
	discovery.RunAgentCardRegistry()
	sep()
	discovery.RunAgentProxy()
	sep()
	discovery.RunBroker()
	sep()

	// Context
	context.RunContextInjection()
	sep()
	context.RunToolProvider()
	sep()

	// Routing
	routing.RunContentBasedRouter()
	sep()
	routing.RunScatterGather()
	sep()
	routing.RunPipeline()
	sep()

	// Coordination
	coordination.RunOrchestrator()
	sep()
	coordination.RunSupervisedDelegation()
	sep()
	coordination.RunChoreography()
	sep()
	coordination.RunPeerToPeerDelegation()
	sep()
	coordination.RunMediator()
	sep()
	coordination.RunGroupChat()
	sep()
	coordination.RunSaga()
	sep()
	coordination.RunMagentic()
	sep()

	// Resilience
	resilience.RunCircuitBreaker()
	sep()
	resilience.RunDeadLetterAgent()
	sep()
	resilience.RunCheckpointResume()
	sep()

	// Implementation
	implementation.RunIdempotentAgent()
	sep()

	// Security
	security.RunLeastPrivilegeToolScope()
	sep()
	security.RunTrustBoundary()
	sep()
	security.RunPromptFirewall()
	sep()

	// Evaluation
	evaluation.RunLLMAsJudge()
	sep()
	evaluation.RunEnsembleJudge()
	sep()
	evaluation.RunReflectionLoop()
}
