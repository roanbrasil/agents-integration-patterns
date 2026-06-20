package routing

import "fmt"

// Pipeline chains a sequence of transformation stages and applies them in order.
func Pipeline(stages []func(string) string, input string) string {
	result := input
	for _, stage := range stages {
		result = stage(result)
	}
	return result
}

// RunPipeline demonstrates the Pipeline pattern.
// Three stages: Fetch -> Transform -> Summarize.
func RunPipeline() {
	fmt.Println("=== Pipeline Pattern ===")

	fetch := func(input string) string {
		out := "[Fetched] raw data about: " + input
		fmt.Printf("  Stage Fetch:     %q\n", out)
		return out
	}

	transform := func(input string) string {
		out := "[Transformed] " + input
		fmt.Printf("  Stage Transform: %q\n", out)
		return out
	}

	summarize := func(input string) string {
		if len(input) > 40 {
			input = input[:40] + "..."
		}
		out := "[Summary] " + input
		fmt.Printf("  Stage Summarize: %q\n", out)
		return out
	}

	stages := []func(string) string{fetch, transform, summarize}
	input := "Go concurrency patterns"

	fmt.Printf("Input: %q\n", input)
	result := Pipeline(stages, input)
	fmt.Printf("Output: %s\n", result)
	fmt.Println()
}
