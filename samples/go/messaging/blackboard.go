package messaging

import (
	"aip-samples/shared"
	"fmt"
	"sync"
)

// Blackboard is a shared memory store protected by a RWMutex.
type Blackboard struct {
	mu   sync.RWMutex
	data map[string]string
}

func newBlackboard() *Blackboard {
	return &Blackboard{data: make(map[string]string)}
}

func (b *Blackboard) Write(key, value string) {
	b.mu.Lock()
	defer b.mu.Unlock()
	b.data[key] = value
}

func (b *Blackboard) Read(key string) string {
	b.mu.RLock()
	defer b.mu.RUnlock()
	return b.data[key]
}

func (b *Blackboard) Keys() []string {
	b.mu.RLock()
	defer b.mu.RUnlock()
	keys := make([]string, 0, len(b.data))
	for k := range b.data {
		keys = append(keys, k)
	}
	return keys
}

// RunBlackboard demonstrates the Blackboard pattern.
// Three goroutines write concurrently; a controller reads all keys afterward.
func RunBlackboard() {
	fmt.Println("=== Blackboard Pattern ===")

	bb := newBlackboard()
	agents := []*shared.FakeAgent{
		shared.NewFakeAgent("Analyst"),
		shared.NewFakeAgent("Researcher"),
		shared.NewFakeAgent("Planner"),
	}
	contributions := []struct{ key, value string }{
		{"analysis", "demand is high"},
		{"research", "competitors are weak"},
		{"plan", "launch next quarter"},
	}

	var wg sync.WaitGroup
	for i, agent := range agents {
		wg.Add(1)
		go func(a *shared.FakeAgent, key, value string) {
			defer wg.Done()
			result := a.Invoke(value)
			bb.Write(key, result)
			fmt.Printf("  [wrote] %s -> %s\n", key, result)
		}(agent, contributions[i].key, contributions[i].value)
	}
	wg.Wait()

	fmt.Println("Controller reads blackboard:")
	for _, k := range bb.Keys() {
		fmt.Printf("  %s: %s\n", k, bb.Read(k))
	}
	fmt.Println()
}
