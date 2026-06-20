package evaluation

import (
	"fmt"
	"strings"
)

// LensJudge evaluates output against a single keyword lens.
type LensJudge struct {
	Name    string
	Keyword string
}

// Evaluate returns true if the output contains the judge's keyword.
func (lj *LensJudge) Evaluate(output string) bool {
	return strings.Contains(strings.ToLower(output), strings.ToLower(lj.Keyword))
}

// Vote returns true if at least half of the results are true.
func Vote(results []bool) bool {
	count := 0
	for _, r := range results {
		if r {
			count++
		}
	}
	return count >= (len(results)+1)/2
}

// RunEnsembleJudge demonstrates the Ensemble Judge evaluation pattern.
func RunEnsembleJudge() {
	fmt.Println("=== Ensemble Judge Pattern ===")

	judges := []*LensJudge{
		{Name: "ClarityJudge", Keyword: "clear"},
		{Name: "FactualJudge", Keyword: "accurate"},
		{Name: "BrevityJudge", Keyword: "concise"},
	}

	outputs := []struct {
		label  string
		output string
	}{
		{"Strong", "This is a clear, accurate, and concise answer."},
		{"Partial", "This is a clear answer but lacks brevity."},
		{"Weak", "Here is some information."},
	}

	for _, o := range outputs {
		fmt.Printf("  Output: %q\n", o.label)
		var results []bool
		for _, j := range judges {
			v := j.Evaluate(o.output)
			results = append(results, v)
			fmt.Printf("    [%s]: %v\n", j.Name, v)
		}
		verdict := Vote(results)
		fmt.Printf("    Ensemble vote: %v\n", verdict)
	}
	fmt.Println()
}
