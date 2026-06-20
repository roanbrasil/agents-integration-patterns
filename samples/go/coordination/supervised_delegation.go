package coordination

import (
	"aip-samples/shared"
	"errors"
	"fmt"
)

// SupervisedDelegation wraps a supervisor-worker pattern with retry on failure.
type SupervisedDelegation struct {
	supervisor *shared.FakeAgent
	worker     *shared.FakeAgent
}

func newSupervisedDelegation() *SupervisedDelegation {
	return &SupervisedDelegation{
		supervisor: shared.NewFakeAgent("Supervisor"),
		worker:     shared.NewFakeAgent("Worker"),
	}
}

func validate(result string) error {
	if result == "" {
		return errors.New("empty result")
	}
	return nil
}

// Delegate sends a task to the worker; on validation failure retries once.
func (sd *SupervisedDelegation) Delegate(task string) (string, error) {
	result := sd.worker.Invoke(task)
	fmt.Printf("  Worker result (attempt 1): %q\n", result)

	if err := validate(result); err != nil {
		fmt.Printf("  Supervisor: validation failed (%v), retrying...\n", err)
		result = sd.worker.Invoke("RETRY: " + task)
		fmt.Printf("  Worker result (attempt 2): %q\n", result)
		if err = validate(result); err != nil {
			return "", fmt.Errorf("delegation failed after retry: %w", err)
		}
	}
	return result, nil
}

// RunSupervisedDelegation demonstrates the Supervised Delegation pattern.
func RunSupervisedDelegation() {
	fmt.Println("=== Supervised Delegation Pattern ===")

	sd := newSupervisedDelegation()
	result, err := sd.Delegate("analyze customer feedback")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	} else {
		fmt.Printf("Final result: %s\n", result)
	}
	fmt.Println()
}
