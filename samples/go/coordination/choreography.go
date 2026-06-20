package coordination

import (
	"aip-samples/shared"
	"fmt"
	"sync"
)

// EventLog is a concurrency-safe append-only log of events.
type EventLog struct {
	mu     sync.Mutex
	events []string
}

func (el *EventLog) Append(event string) {
	el.mu.Lock()
	defer el.mu.Unlock()
	el.events = append(el.events, event)
}

func (el *EventLog) Last() string {
	el.mu.Lock()
	defer el.mu.Unlock()
	if len(el.events) == 0 {
		return ""
	}
	return el.events[len(el.events)-1]
}

func (el *EventLog) All() []string {
	el.mu.Lock()
	defer el.mu.Unlock()
	cp := make([]string, len(el.events))
	copy(cp, el.events)
	return cp
}

// RunChoreography demonstrates the Choreography pattern.
// Agents react to each other's events without a central orchestrator.
func RunChoreography() {
	fmt.Println("=== Choreography Pattern ===")

	log := &EventLog{}
	agents := []*shared.FakeAgent{
		shared.NewFakeAgent("AgentAlpha"),
		shared.NewFakeAgent("AgentBeta"),
		shared.NewFakeAgent("AgentGamma"),
	}

	for _, agent := range agents {
		last := log.Last()
		var event string
		if last == "" {
			event = agent.Invoke("starting workflow")
		} else {
			event = agent.Invoke("reacting to: " + last)
		}
		log.Append(event)
	}

	fmt.Println("Event log:")
	for i, e := range log.All() {
		fmt.Printf("  [%d] %s\n", i+1, e)
	}
	fmt.Println()
}
