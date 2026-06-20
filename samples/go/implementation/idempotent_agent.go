package implementation

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"sync"
)

// IdempotentAgent caches results by operation ID to avoid recomputing.
type IdempotentAgent struct {
	mu    sync.Mutex
	store map[string]string
}

func newIdempotentAgent() *IdempotentAgent {
	return &IdempotentAgent{store: make(map[string]string)}
}

// Execute returns a cached result for the given opID, or computes and stores it.
func (ia *IdempotentAgent) Execute(opID, prompt string) (string, bool) {
	ia.mu.Lock()
	defer ia.mu.Unlock()

	if cached, ok := ia.store[opID]; ok {
		return cached, true // cache hit
	}

	// Compute: SHA-256 of the prompt as a deterministic "result"
	h := sha256.Sum256([]byte(prompt))
	result := "result:" + hex.EncodeToString(h[:8])
	ia.store[opID] = result
	return result, false
}

// RunIdempotentAgent demonstrates the Idempotent Agent pattern.
func RunIdempotentAgent() {
	fmt.Println("=== Idempotent Agent Pattern ===")

	agent := newIdempotentAgent()

	calls := []struct{ opID, prompt string }{
		{"op-1", "summarize the quarterly report"},
		{"op-2", "translate document to Spanish"},
		{"op-1", "summarize the quarterly report"}, // duplicate
		{"op-3", "generate meeting notes"},
		{"op-2", "translate document to Spanish"}, // duplicate
	}

	for _, c := range calls {
		result, cached := agent.Execute(c.opID, c.prompt)
		status := "computed"
		if cached {
			status = "CACHE HIT"
		}
		fmt.Printf("  opID=%s [%s]: %s\n", c.opID, status, result)
	}
	fmt.Println()
}
