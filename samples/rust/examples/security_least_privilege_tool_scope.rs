// Pattern: Least Privilege Tool Scope
// Agents are granted minimum required permissions; higher-privilege calls are denied.

#[derive(Debug, Clone, PartialEq, PartialOrd)]
enum ToolScope { ReadOnly = 0, ReadWrite = 1, Admin = 2 }

struct ScopedAgent {
    name: String,
    scope: ToolScope,
}

struct ToolCall {
    name: String,
    required_scope: ToolScope,
}

impl ScopedAgent {
    fn new(name: &str, scope: ToolScope) -> Self {
        Self { name: name.to_string(), scope }
    }

    fn call_tool(&self, tool: &ToolCall) -> Result<String, String> {
        if self.scope >= tool.required_scope {
            Ok(format!("{} executed '{}' (scope={:?})", self.name, tool.name, self.scope))
        } else {
            Err(format!("{} DENIED '{}': needs {:?} but has {:?}",
                self.name, tool.name, tool.required_scope, self.scope))
        }
    }
}

fn main() {
    println!("=== LeastPrivilegeToolScope Pattern ===\n");

    let agents = vec![
        ScopedAgent::new("ReadAgent",  ToolScope::ReadOnly),
        ScopedAgent::new("WriteAgent", ToolScope::ReadWrite),
        ScopedAgent::new("AdminAgent", ToolScope::Admin),
    ];

    let tools = vec![
        ToolCall { name: "read_file".to_string(),   required_scope: ToolScope::ReadOnly  },
        ToolCall { name: "write_file".to_string(),  required_scope: ToolScope::ReadWrite },
        ToolCall { name: "delete_all".to_string(),  required_scope: ToolScope::Admin     },
    ];

    for agent in &agents {
        println!("Agent: {} (scope={:?})", agent.name, agent.scope);
        for tool in &tools {
            match agent.call_tool(tool) {
                Ok(msg)  => println!("  [OK]    {}", msg),
                Err(msg) => println!("  [DENY]  {}", msg),
            }
        }
        println!();
    }
}
