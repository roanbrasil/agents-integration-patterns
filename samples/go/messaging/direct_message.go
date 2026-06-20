package messaging

import (
	"aip-samples/shared"
	"fmt"
)

// Run demonstrates the Direct Message pattern.
// AgentA sends a question to AgentB via a Go channel.
func RunDirectMessage() {
	fmt.Println("=== Direct Message Pattern ===")

	agentA := shared.NewFakeAgent("AgentA")
	agentB := shared.NewFakeAgent("AgentB")

	requestCh := make(chan string, 1)
	responseCh := make(chan string, 1)

	// AgentA sends a question
	go func() {
		question := agentA.Invoke("What is the capital of France?")
		fmt.Printf("AgentA sends: %s\n", question)
		requestCh <- question
	}()

	// AgentB receives and responds
	go func() {
		msg := <-requestCh
		response := agentB.Invoke("Responding to: " + msg)
		fmt.Printf("AgentB responds: %s\n", response)
		responseCh <- response
	}()

	result := <-responseCh
	fmt.Printf("Final result: %s\n", result)
	fmt.Println()
}
