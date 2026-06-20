package routing

import (
	"aip-samples/shared"
	"fmt"
	"strings"
)

// ContentBasedRouter routes tasks to agents based on content keywords.
type ContentBasedRouter struct {
	codeAgent     *shared.FakeAgent
	researchAgent *shared.FakeAgent
	defaultAgent  *shared.FakeAgent
}

func newContentBasedRouter() *ContentBasedRouter {
	return &ContentBasedRouter{
		codeAgent:     shared.NewFakeAgent("CodeAgent"),
		researchAgent: shared.NewFakeAgent("ResearchAgent"),
		defaultAgent:  shared.NewFakeAgent("DefaultAgent"),
	}
}

// Route dispatches the task to the appropriate agent based on its content.
func (r *ContentBasedRouter) Route(task string) string {
	lower := strings.ToLower(task)
	switch {
	case strings.Contains(lower, "code"):
		return r.codeAgent.Invoke(task)
	case strings.Contains(lower, "research"):
		return r.researchAgent.Invoke(task)
	default:
		return r.defaultAgent.Invoke(task)
	}
}

// RunContentBasedRouter demonstrates the Content-Based Router pattern.
func RunContentBasedRouter() {
	fmt.Println("=== Content-Based Router Pattern ===")

	router := newContentBasedRouter()

	tasks := []string{
		"write code to sort a list",
		"research the history of the internet",
		"schedule a meeting for tomorrow",
	}

	for _, task := range tasks {
		result := router.Route(task)
		fmt.Printf("Task: %q\n  -> %s\n", task, result)
	}
	fmt.Println()
}
