package context

import (
	"aip-samples/shared"
	"fmt"
	"strings"
)

// ContextAssembler assembles context documents and injects them into agent prompts.
type ContextAssembler struct {
	docs []string
}

func newContextAssembler(docs []string) *ContextAssembler {
	return &ContextAssembler{docs: docs}
}

// Inject prepends the assembled context to the given prompt.
func (ca *ContextAssembler) Inject(prompt string) string {
	context := strings.Join(ca.docs, "\n---\n")
	return context + "\n\n" + prompt
}

// RunContextInjection demonstrates the Context Injection pattern.
func RunContextInjection() {
	fmt.Println("=== Context Injection Pattern ===")

	docs := []string{
		"Document 1: Go is a statically typed, compiled language.",
		"Document 2: Go was designed at Google in 2007.",
		"Document 3: Go emphasizes simplicity and concurrency.",
	}

	assembler := newContextAssembler(docs)
	agent := shared.NewFakeAgent("RAGAgent")

	userQuery := "Summarize what you know about Go."
	enrichedPrompt := assembler.Inject(userQuery)

	fmt.Printf("Injected prompt length: %d chars\n", len(enrichedPrompt))
	fmt.Printf("User query: %q\n", userQuery)

	response := agent.Invoke(enrichedPrompt)
	fmt.Printf("Agent response: %s\n", response)
	fmt.Println()
}
