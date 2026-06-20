package resilience

import (
	"fmt"
)

// RunDeadLetterAgent demonstrates the Dead Letter Agent pattern.
// Tasks are retried up to 3 times; permanently failed tasks go to a DLQ.
func RunDeadLetterAgent() {
	fmt.Println("=== Dead Letter Agent Pattern ===")

	tasks := []string{"task-A", "task-B", "task-C", "task-D"}
	maxRetries := 3

	// Simulate: task-B always fails, all others succeed on first try
	alwaysFails := map[string]bool{"task-B": true}

	var dlq []string

	for _, task := range tasks {
		success := false
		for attempt := 1; attempt <= maxRetries; attempt++ {
			if alwaysFails[task] {
				fmt.Printf("  [%s] attempt %d: FAILED\n", task, attempt)
			} else {
				fmt.Printf("  [%s] attempt %d: OK\n", task, attempt)
				success = true
				break
			}
		}
		if !success {
			dlq = append(dlq, task)
			fmt.Printf("  [%s] moved to DLQ after %d failures\n", task, maxRetries)
		}
	}

	fmt.Printf("Main queue processed: %d tasks\n", len(tasks)-len(dlq))
	fmt.Printf("Dead Letter Queue:    %v\n", dlq)
	fmt.Println()
}
