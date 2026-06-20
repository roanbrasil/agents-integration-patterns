package discovery

import (
	"aip-samples/shared"
	"fmt"
	"strings"
)

// AgentProxy wraps a FakeAgent and transparently translates prompts before forwarding.
type AgentProxy struct {
	backend *shared.FakeAgent
}

func newAgentProxy(backend *shared.FakeAgent) *AgentProxy {
	return &AgentProxy{backend: backend}
}

// Invoke translates the prompt (uppercases it) then forwards to the backend agent.
func (p *AgentProxy) Invoke(prompt string) string {
	translated := strings.ToUpper(prompt)
	return p.backend.Invoke(translated)
}

// RunAgentProxy demonstrates the Agent Proxy pattern.
func RunAgentProxy() {
	fmt.Println("=== Agent Proxy Pattern ===")

	backend := shared.NewFakeAgent("BackendAgent")
	proxy := newAgentProxy(backend)

	original := "process this task quietly"
	fmt.Printf("Caller sends:    %q\n", original)

	result := proxy.Invoke(original)
	fmt.Printf("Proxy forwards (uppercased) and backend responds:\n  %s\n", result)
	fmt.Println()
}
