package messaging

import (
	"aip-samples/shared"
	"fmt"
	"sync"
)

// Run demonstrates the Broadcast Message pattern.
// Publisher sends one message to 3 subscriber FakeAgents via a fan-out channel.
func RunBroadcastMessage() {
	fmt.Println("=== Broadcast Message Pattern ===")

	subscribers := []*shared.FakeAgent{
		shared.NewFakeAgent("Subscriber-1"),
		shared.NewFakeAgent("Subscriber-2"),
		shared.NewFakeAgent("Subscriber-3"),
	}

	topic := "System maintenance at midnight"

	var wg sync.WaitGroup
	for _, sub := range subscribers {
		wg.Add(1)
		go func(agent *shared.FakeAgent) {
			defer wg.Done()
			response := agent.Invoke(topic)
			fmt.Printf("  %s\n", response)
		}(sub)
	}

	fmt.Printf("Publisher broadcasting: %q\n", topic)
	wg.Wait()
	fmt.Println("All subscribers processed the broadcast.")
	fmt.Println()
}
