package security

import "fmt"

// Scope defines the permission level of an agent.
type Scope int

const (
	ScopeRead  Scope = 1
	ScopeWrite Scope = 2
	ScopeAdmin Scope = 3
)

func (s Scope) String() string {
	switch s {
	case ScopeRead:
		return "Read"
	case ScopeWrite:
		return "Write"
	case ScopeAdmin:
		return "Admin"
	default:
		return "Unknown"
	}
}

// ScopedAgent is an agent with a fixed permission scope.
type ScopedAgent struct {
	Name  string
	Scope Scope
}

// CanCall returns true if the agent's scope meets or exceeds the required scope.
func (a *ScopedAgent) CanCall(requiredScope Scope) bool {
	return a.Scope >= requiredScope
}

// RunLeastPrivilegeToolScope demonstrates the Least-Privilege Tool Scope pattern.
func RunLeastPrivilegeToolScope() {
	fmt.Println("=== Least Privilege Tool Scope Pattern ===")

	readOnlyAgent := &ScopedAgent{Name: "ReadOnlyAgent", Scope: ScopeRead}
	writeAgent := &ScopedAgent{Name: "WriteAgent", Scope: ScopeWrite}
	adminAgent := &ScopedAgent{Name: "AdminAgent", Scope: ScopeAdmin}

	checks := []struct {
		agent    *ScopedAgent
		required Scope
		tool     string
	}{
		{readOnlyAgent, ScopeRead, "read_file"},
		{readOnlyAgent, ScopeWrite, "write_file"},
		{writeAgent, ScopeWrite, "write_file"},
		{writeAgent, ScopeAdmin, "delete_all"},
		{adminAgent, ScopeAdmin, "delete_all"},
	}

	for _, c := range checks {
		allowed := c.agent.CanCall(c.required)
		status := "ALLOWED"
		if !allowed {
			status = "BLOCKED"
		}
		fmt.Printf("  [%s] %s -> tool=%s (requires %s): %s\n",
			c.agent.Name, c.agent.Scope, c.tool, c.required, status)
	}
	fmt.Println()
}
