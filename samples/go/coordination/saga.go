package coordination

import (
	"errors"
	"fmt"
)

// SagaStep defines a saga step with an execute and compensate action.
type SagaStep struct {
	Name       string
	Execute    func() error
	Compensate func()
}

// RunSaga demonstrates the Saga pattern.
// Step 2 fails, triggering compensation for completed steps in reverse.
func RunSaga() {
	fmt.Println("=== Saga Pattern ===")

	var sagaLog []string
	log := func(msg string) {
		sagaLog = append(sagaLog, msg)
		fmt.Printf("  %s\n", msg)
	}

	steps := []SagaStep{
		{
			Name:       "ReserveInventory",
			Execute:    func() error { log("ReserveInventory: reserved 10 units"); return nil },
			Compensate: func() { log("ReserveInventory: released 10 units (compensation)") },
		},
		{
			Name: "ChargePayment",
			Execute: func() error {
				log("ChargePayment: attempting charge...")
				return errors.New("payment gateway timeout")
			},
			Compensate: func() { log("ChargePayment: refunded (compensation)") },
		},
		{
			Name:       "ShipOrder",
			Execute:    func() error { log("ShipOrder: dispatched"); return nil },
			Compensate: func() { log("ShipOrder: cancelled shipment (compensation)") },
		},
	}

	var completed []SagaStep
	var failed bool
	for _, step := range steps {
		if err := step.Execute(); err != nil {
			fmt.Printf("  SAGA FAILURE at %s: %v\n", step.Name, err)
			failed = true
			break
		}
		completed = append(completed, step)
	}

	if failed {
		fmt.Println("  Running compensations in reverse:")
		for i := len(completed) - 1; i >= 0; i-- {
			completed[i].Compensate()
		}
	}

	fmt.Printf("Saga log has %d entries.\n", len(sagaLog))
	fmt.Println()
}
