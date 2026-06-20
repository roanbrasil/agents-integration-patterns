package discovery

import (
	"fmt"
	"strings"
)

// Provider describes a service provider with a name, capability, and quality score.
type Provider struct {
	Name       string
	Capability string
	Score      float64
}

// Broker routes tasks to the best-matching provider.
type Broker struct {
	providers []Provider
}

func newBroker() *Broker {
	return &Broker{}
}

func (b *Broker) Register(p Provider) {
	b.providers = append(b.providers, p)
}

// Route filters providers by keyword match in the task and picks the highest score.
func (b *Broker) Route(task string) (Provider, bool) {
	var best Provider
	found := false
	for _, p := range b.providers {
		if strings.Contains(strings.ToLower(task), strings.ToLower(p.Capability)) {
			if !found || p.Score > best.Score {
				best = p
				found = true
			}
		}
	}
	return best, found
}

// RunBroker demonstrates the Broker pattern.
func RunBroker() {
	fmt.Println("=== Broker Pattern ===")

	broker := newBroker()
	broker.Register(Provider{Name: "SearchA", Capability: "search", Score: 0.7})
	broker.Register(Provider{Name: "SearchB", Capability: "search", Score: 0.95})
	broker.Register(Provider{Name: "Analyzer", Capability: "analyze", Score: 0.8})

	tasks := []string{
		"please search the web for Go patterns",
		"analyze the sales data",
		"translate this document",
	}
	for _, task := range tasks {
		if p, ok := broker.Route(task); ok {
			fmt.Printf("Task: %q -> routed to %s (score=%.2f)\n", task, p.Name, p.Score)
		} else {
			fmt.Printf("Task: %q -> no provider found\n", task)
		}
	}
	fmt.Println()
}
