package routing

import (
	"aip-samples/shared"
	"fmt"
	"sync"
)

// RunScatterGather demonstrates the Scatter-Gather pattern.
// A task is fanned out to multiple agents concurrently; all results are collected.
func RunScatterGather() {
	fmt.Println("=== Scatter-Gather Pattern ===")

	agents := []*shared.FakeAgent{
		shared.NewFakeAgent("ExpertA"),
		shared.NewFakeAgent("ExpertB"),
		shared.NewFakeAgent("ExpertC"),
	}

	task := "evaluate the market opportunity"

	var (
		mu      sync.Mutex
		results []string
		wg      sync.WaitGroup
	)

	for _, agent := range agents {
		wg.Add(1)
		go func(a *shared.FakeAgent) {
			defer wg.Done()
			res := a.Invoke(task)
			mu.Lock()
			results = append(results, res)
			mu.Unlock()
		}(agent)
	}

	wg.Wait()

	fmt.Printf("Scattered task to %d agents: %q\n", len(agents), task)
	fmt.Println("Gathered results:")
	for _, r := range results {
		fmt.Printf("  %s\n", r)
	}
	fmt.Println()
}
