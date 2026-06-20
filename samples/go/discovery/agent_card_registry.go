package discovery

import "fmt"

// AgentCard describes an agent's identity and capabilities.
type AgentCard struct {
	Name         string
	Capabilities []string
}

// Registry holds registered AgentCards by name.
type Registry struct {
	cards map[string]AgentCard
}

func newRegistry() *Registry {
	return &Registry{cards: make(map[string]AgentCard)}
}

// Register adds an AgentCard to the registry.
func (r *Registry) Register(card AgentCard) {
	r.cards[card.Name] = card
}

// FindByCapability returns agent names that have the given capability.
func (r *Registry) FindByCapability(cap string) []string {
	var results []string
	for _, card := range r.cards {
		for _, c := range card.Capabilities {
			if c == cap {
				results = append(results, card.Name)
				break
			}
		}
	}
	return results
}

// RunAgentCardRegistry demonstrates the Agent Card Registry pattern.
func RunAgentCardRegistry() {
	fmt.Println("=== Agent Card Registry Pattern ===")

	reg := newRegistry()
	reg.Register(AgentCard{Name: "DataAgent", Capabilities: []string{"search", "analytics"}})
	reg.Register(AgentCard{Name: "WriteAgent", Capabilities: []string{"write", "summarize"}})
	reg.Register(AgentCard{Name: "SearchAgent", Capabilities: []string{"search", "web"}})

	fmt.Println("Registered 3 agents.")

	cap := "search"
	found := reg.FindByCapability(cap)
	fmt.Printf("Agents with capability %q: %v\n", cap, found)

	cap2 := "summarize"
	found2 := reg.FindByCapability(cap2)
	fmt.Printf("Agents with capability %q: %v\n", cap2, found2)
	fmt.Println()
}
