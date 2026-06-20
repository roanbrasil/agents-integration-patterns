package evaluation

import (
	"fmt"
	"strings"
)

// Generator produces a draft, optionally incorporating critique.
type Generator struct {
	name string
}

// Generate returns a draft. On second+ iteration (critique non-empty) it adds the required keyword.
func (g *Generator) Generate(task, critique string) string {
	if critique == "" {
		return fmt.Sprintf("[%s] Draft: here is a response to: %s", g.name, task)
	}
	// Incorporate critique: add the missing keyword
	missing := strings.TrimPrefix(critique, "missing keyword: ")
	missing = strings.Trim(missing, `"`)
	return fmt.Sprintf("[%s] Revised: %s response (now %s)", g.name, task, missing)
}

// Critic evaluates a draft and returns (pass, feedback).
type Critic struct {
	required string
}

// Evaluate checks if the draft contains the required keyword.
func (c *Critic) Evaluate(draft string) (bool, string) {
	if strings.Contains(strings.ToLower(draft), strings.ToLower(c.required)) {
		return true, "approved"
	}
	return false, fmt.Sprintf("missing keyword: %q", c.required)
}

// RunReflectionLoop demonstrates the Reflection Loop evaluation pattern.
func RunReflectionLoop() {
	fmt.Println("=== Reflection Loop Pattern ===")

	gen := &Generator{name: "Drafter"}
	critic := &Critic{required: "concise"}

	task := "explain Go interfaces"
	maxIter := 3
	critique := ""

	for i := 1; i <= maxIter; i++ {
		draft := gen.Generate(task, critique)
		fmt.Printf("  Iteration %d draft:   %s\n", i, draft)

		pass, feedback := critic.Evaluate(draft)
		fmt.Printf("  Iteration %d verdict: %s\n", i, feedback)

		if pass {
			fmt.Printf("  Converged at iteration %d.\n", i)
			break
		}
		critique = feedback
	}
	fmt.Println()
}
