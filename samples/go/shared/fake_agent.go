package shared

import "fmt"

// FakeAgent simulates an AI agent without requiring a real API key.
type FakeAgent struct {
	Name string
}

// NewFakeAgent creates a new FakeAgent with the given name.
func NewFakeAgent(name string) *FakeAgent {
	return &FakeAgent{Name: name}
}

// Invoke simulates invoking the agent with a prompt and returns a deterministic response.
func (a *FakeAgent) Invoke(prompt string) string {
	if len(prompt) > 60 {
		prompt = prompt[:60]
	}
	return fmt.Sprintf("[%s] %s", a.Name, prompt)
}
