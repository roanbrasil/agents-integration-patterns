package evaluation

import (
	"fmt"
	"strings"
)

// Judge evaluates an agent output against a rubric of required keywords.
type Judge struct{}

// Evaluate returns (pass, reason). Fails on the first missing rubric keyword.
func (j *Judge) Evaluate(output string, rubric []string) (bool, string) {
	lower := strings.ToLower(output)
	for _, keyword := range rubric {
		if !strings.Contains(lower, strings.ToLower(keyword)) {
			return false, fmt.Sprintf("missing required keyword: %q", keyword)
		}
	}
	return true, "all rubric criteria satisfied"
}

// RunLLMAsJudge demonstrates the LLM-as-Judge evaluation pattern.
func RunLLMAsJudge() {
	fmt.Println("=== LLM-as-Judge Pattern ===")

	judge := &Judge{}
	rubric := []string{"concise", "accurate", "cited"}

	cases := []struct {
		name   string
		output string
	}{
		{
			name:   "Good output",
			output: "This is a concise and accurate summary with cited sources.",
		},
		{
			name:   "Missing citation",
			output: "This is a concise and accurate summary.",
		},
		{
			name:   "Too vague",
			output: "Here is some information.",
		},
	}

	for _, c := range cases {
		pass, reason := judge.Evaluate(c.output, rubric)
		status := "PASS"
		if !pass {
			status = "FAIL"
		}
		fmt.Printf("  [%s] %s: %s\n", status, c.name, reason)
	}
	fmt.Println()
}
