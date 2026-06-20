package context

import (
	"fmt"
	"sort"
)

// Tool represents a callable tool with a name and a function.
type Tool struct {
	Name string
	Fn   func(string) string
}

// ToolRegistry holds a collection of named tools.
type ToolRegistry struct {
	tools map[string]Tool
}

func newToolRegistry() *ToolRegistry {
	return &ToolRegistry{tools: make(map[string]Tool)}
}

// Register adds a tool to the registry.
func (tr *ToolRegistry) Register(t Tool) {
	tr.tools[t.Name] = t
}

// List returns sorted tool names available in the registry.
func (tr *ToolRegistry) List() []string {
	names := make([]string, 0, len(tr.tools))
	for name := range tr.tools {
		names = append(names, name)
	}
	sort.Strings(names)
	return names
}

// Call invokes the named tool with the given args.
func (tr *ToolRegistry) Call(name, args string) string {
	if t, ok := tr.tools[name]; ok {
		return t.Fn(args)
	}
	return fmt.Sprintf("error: tool %q not found", name)
}

// RunToolProvider demonstrates the Tool Provider pattern.
func RunToolProvider() {
	fmt.Println("=== Tool Provider Pattern ===")

	reg := newToolRegistry()
	reg.Register(Tool{Name: "calculator", Fn: func(args string) string {
		return "result of " + args + " = 42"
	}})
	reg.Register(Tool{Name: "weather", Fn: func(args string) string {
		return "weather in " + args + " is sunny"
	}})
	reg.Register(Tool{Name: "clock", Fn: func(_ string) string {
		return "current time is 12:00 UTC"
	}})

	fmt.Printf("Available tools: %v\n", reg.List())

	fmt.Printf("Call calculator(2+2*10): %s\n", reg.Call("calculator", "2+2*10"))
	fmt.Printf("Call weather(London):    %s\n", reg.Call("weather", "London"))
	fmt.Printf("Call unknown:            %s\n", reg.Call("unknown", ""))
	fmt.Println()
}
