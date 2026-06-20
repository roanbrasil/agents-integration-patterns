package coordination

import "fmt"

// WorkerStep is a named step with a function that transforms state.
type WorkerStep struct {
	Name string
	Fn   func(map[string]string) map[string]string
}

// Orchestrator runs steps sequentially, threading state through each.
type Orchestrator struct {
	steps []WorkerStep
}

func newOrchestrator(steps []WorkerStep) *Orchestrator {
	return &Orchestrator{steps: steps}
}

// Run executes all steps in order and returns the final state.
func (o *Orchestrator) Run(initialState map[string]string) map[string]string {
	state := initialState
	for _, step := range o.steps {
		fmt.Printf("  [%s] running...\n", step.Name)
		state = step.Fn(state)
		for k, v := range state {
			fmt.Printf("    state[%s] = %s\n", k, v)
		}
	}
	return state
}

// RunOrchestrator demonstrates the Orchestrator pattern.
func RunOrchestrator() {
	fmt.Println("=== Orchestrator Pattern ===")

	steps := []WorkerStep{
		{
			Name: "Gather",
			Fn: func(s map[string]string) map[string]string {
				s["data"] = "raw metrics collected"
				return s
			},
		},
		{
			Name: "Analyze",
			Fn: func(s map[string]string) map[string]string {
				s["analysis"] = "trends identified in: " + s["data"]
				return s
			},
		},
		{
			Name: "Report",
			Fn: func(s map[string]string) map[string]string {
				s["report"] = "executive summary based on: " + s["analysis"]
				return s
			},
		},
	}

	orch := newOrchestrator(steps)
	orch.Run(map[string]string{})
	fmt.Println()
}
