package resilience

import (
	"errors"
	"fmt"
	"time"
)

const (
	stateClosed   = "CLOSED"
	stateOpen     = "OPEN"
	stateHalfOpen = "HALF_OPEN"
)

// CircuitBreaker prevents repeated calls to a failing service.
type CircuitBreaker struct {
	state        string
	failureCount int
	threshold    int
	openedAt     time.Time
	timeout      time.Duration
}

func newCircuitBreaker(threshold int, timeout time.Duration) *CircuitBreaker {
	return &CircuitBreaker{state: stateClosed, threshold: threshold, timeout: timeout}
}

// Call executes fn through the circuit breaker.
func (cb *CircuitBreaker) Call(fn func() error) error {
	switch cb.state {
	case stateOpen:
		if time.Since(cb.openedAt) > cb.timeout {
			cb.state = stateHalfOpen
			fmt.Println("  CircuitBreaker: OPEN -> HALF_OPEN (timeout elapsed)")
		} else {
			return errors.New("circuit OPEN: request rejected")
		}
	}

	err := fn()
	if err != nil {
		cb.failureCount++
		fmt.Printf("  CircuitBreaker: failure #%d\n", cb.failureCount)
		if cb.failureCount >= cb.threshold {
			cb.state = stateOpen
			cb.openedAt = time.Now()
			fmt.Printf("  CircuitBreaker: CLOSED -> OPEN (threshold %d reached)\n", cb.threshold)
		}
		return err
	}

	// Success
	if cb.state == stateHalfOpen {
		fmt.Println("  CircuitBreaker: HALF_OPEN -> CLOSED (recovered)")
	}
	cb.state = stateClosed
	cb.failureCount = 0
	return nil
}

// RunCircuitBreaker demonstrates the Circuit Breaker pattern.
func RunCircuitBreaker() {
	fmt.Println("=== Circuit Breaker Pattern ===")

	cb := newCircuitBreaker(2, 50*time.Millisecond)

	fail := func() error { return errors.New("service unavailable") }
	succeed := func() error { return nil }

	for i := 1; i <= 3; i++ {
		err := cb.Call(fail)
		fmt.Printf("  Call %d: %v | state=%s\n", i, err, cb.state)
	}

	// Wait for timeout to expire
	time.Sleep(60 * time.Millisecond)

	err := cb.Call(succeed)
	fmt.Printf("  Recovery call: err=%v | state=%s\n", err, cb.state)
	fmt.Println()
}
