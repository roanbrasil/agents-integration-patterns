package coordination

import (
	"fmt"
	"strings"
)

// P2PAgent handles tasks or delegates to the next agent in the chain.
type P2PAgent struct {
	name string
	next *P2PAgent
	// canHandle returns true if this agent can handle the task.
	canHandle func(task string) bool
}

func (a *P2PAgent) Handle(task string) string {
	if a.canHandle(task) {
		return fmt.Sprintf("[%s] handled: %s", a.name, task)
	}
	if a.next != nil {
		fmt.Printf("  [%s] cannot handle, delegating to %s\n", a.name, a.next.name)
		return a.next.Handle(task)
	}
	return fmt.Sprintf("[%s] no handler found for: %s", a.name, task)
}

// RunPeerToPeerDelegation demonstrates the Peer-to-Peer Delegation pattern.
func RunPeerToPeerDelegation() {
	fmt.Println("=== Peer-to-Peer Delegation Pattern ===")

	agentC := &P2PAgent{
		name: "AgentC",
		canHandle: func(task string) bool {
			return strings.Contains(task, "translate")
		},
	}
	agentB := &P2PAgent{
		name: "AgentB",
		next: agentC,
		canHandle: func(task string) bool {
			return strings.Contains(task, "language")
		},
	}
	agentA := &P2PAgent{
		name: "AgentA",
		next: agentB,
		canHandle: func(task string) bool {
			return strings.Contains(task, "2+2")
		},
	}

	tasks := []string{
		"calculate 2+2",
		"fix language grammar",
		"translate this sentence to French",
	}

	for _, task := range tasks {
		fmt.Printf("Task: %q\n", task)
		result := agentA.Handle(task)
		fmt.Printf("  Result: %s\n", result)
	}
	fmt.Println()
}
