package resilience

import (
	"fmt"
)

// Checkpoint holds the last completed step and its associated state.
type Checkpoint struct {
	Step  int
	State string
}

// RunCheckpointResume demonstrates the Checkpoint & Resume pattern.
// Simulates a crash at step 3 of 5, then resumes from the saved checkpoint.
func RunCheckpointResume() {
	fmt.Println("=== Checkpoint & Resume Pattern ===")

	crashAt := 3 // simulate crash before completing this step (out of 5 total)

	steps := []string{
		"Load data",
		"Validate schema",
		"Transform records",
		"Enrich with metadata",
		"Write output",
	}

	// --- First run: crash at step crashAt ---
	fmt.Println("First run (crashes at step 3):")
	var ckpt Checkpoint
	for i, name := range steps {
		step := i + 1
		if step == crashAt {
			fmt.Printf("  Step %d [%s]: CRASH — saving checkpoint at step %d\n", step, name, i)
			break
		}
		fmt.Printf("  Step %d [%s]: done\n", step, name)
		ckpt = Checkpoint{Step: step, State: fmt.Sprintf("after-%s", name)}
	}
	fmt.Printf("  Checkpoint saved: %+v\n", ckpt)

	// --- Resume run: skip completed steps ---
	fmt.Printf("\nResume run (from checkpoint step %d):\n", ckpt.Step)
	for i, name := range steps {
		step := i + 1
		if step <= ckpt.Step {
			fmt.Printf("  Step %d [%s]: skipping (already done)\n", step, name)
			continue
		}
		fmt.Printf("  Step %d [%s]: done\n", step, name)
	}
	fmt.Println("  All steps completed.")
	fmt.Println()
}
