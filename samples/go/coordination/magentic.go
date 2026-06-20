package coordination

import (
	"aip-samples/shared"
	"fmt"
)

// MagenticOrchestrator runs tasks with deduplication via a ledger.
type MagenticOrchestrator struct {
	agent  *shared.FakeAgent
	ledger map[string]bool
}

func newMagenticOrchestrator() *MagenticOrchestrator {
	return &MagenticOrchestrator{
		agent:  shared.NewFakeAgent("MagenticAgent"),
		ledger: make(map[string]bool),
	}
}

// Run processes tasks, skipping any already recorded in the ledger.
func (mo *MagenticOrchestrator) Run(tasks []string) {
	for _, task := range tasks {
		if mo.ledger[task] {
			fmt.Printf("  [SKIP] already completed: %q\n", task)
			continue
		}
		result := mo.agent.Invoke(task)
		mo.ledger[task] = true
		fmt.Printf("  [DONE] %s\n", result)
	}
}

// RunMagentic demonstrates the Magentic-One orchestration pattern with deduplication.
func RunMagentic() {
	fmt.Println("=== Magentic Pattern ===")

	orch := newMagenticOrchestrator()

	// First pass
	fmt.Println("First run:")
	orch.Run([]string{"fetch data", "analyze data", "write report"})

	// Second pass — some tasks already done
	fmt.Println("Second run (with duplicates):")
	orch.Run([]string{"fetch data", "send email", "analyze data"})

	fmt.Printf("Ledger contains %d unique completed tasks.\n", len(orch.ledger))
	fmt.Println()
}
