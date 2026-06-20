// Pattern: Tool Provider
// Agent calls named tools from a registry to extend its capabilities.

struct Tool {
    name: String,
    handler: Box<dyn Fn(&str) -> String>,
}

struct ToolRegistry {
    tools: Vec<Tool>,
}

impl ToolRegistry {
    fn new() -> Self { Self { tools: Vec::new() } }

    fn register(&mut self, name: &str, handler: impl Fn(&str) -> String + 'static) {
        self.tools.push(Tool { name: name.to_string(), handler: Box::new(handler) });
    }

    fn list(&self) -> Vec<&str> {
        self.tools.iter().map(|t| t.name.as_str()).collect()
    }

    fn call(&self, tool_name: &str, args: &str) -> Result<String, String> {
        self.tools
            .iter()
            .find(|t| t.name == tool_name)
            .map(|t| (t.handler)(args))
            .ok_or_else(|| format!("Tool '{}' not found", tool_name))
    }
}

fn main() {
    println!("=== ToolProvider Pattern ===");

    let mut registry = ToolRegistry::new();
    registry.register("calculator", |args| format!("calc({}) = 42", args));
    registry.register("web_search", |args| format!("results for '{}': [article1, article2]", args));
    registry.register("file_read",  |args| format!("contents of '{}': Hello, World!", args));

    println!("tools/list: {:?}\n", registry.list());

    let calls = vec![
        ("calculator", "2 + 2"),
        ("web_search", "Rust async patterns"),
        ("unknown_tool", "test"),
    ];

    for (tool, args) in &calls {
        match registry.call(tool, args) {
            Ok(result) => println!("tools/call '{}' args='{}' -> {}", tool, args, result),
            Err(e)     => println!("tools/call '{}' args='{}' -> ERROR: {}", tool, args, e),
        }
    }
}
