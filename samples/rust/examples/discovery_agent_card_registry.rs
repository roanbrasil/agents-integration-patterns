// Pattern: Agent Card Registry
// Agents register capability cards; callers query by capability to find agents.

fn main() {
    println!("=== AgentCardRegistry Pattern ===");

    #[derive(Debug)]
    struct AgentCard {
        name: String,
        capabilities: Vec<String>,
    }

    struct Registry {
        cards: Vec<AgentCard>,
    }

    impl Registry {
        fn new() -> Self { Self { cards: Vec::new() } }

        fn register(&mut self, name: &str, capabilities: Vec<&str>) {
            self.cards.push(AgentCard {
                name: name.to_string(),
                capabilities: capabilities.iter().map(|s| s.to_string()).collect(),
            });
        }

        fn query(&self, capability: &str) -> Vec<&str> {
            self.cards
                .iter()
                .filter(|c| c.capabilities.iter().any(|cap| cap == capability))
                .map(|c| c.name.as_str())
                .collect()
        }
    }

    let mut registry = Registry::new();
    registry.register("ResearchAgent", vec!["search", "summarize"]);
    registry.register("CodeAgent",     vec!["code", "debug"]);
    registry.register("DataAgent",     vec!["search", "analyze"]);

    println!("Registered 3 agents.\n");

    for cap in &["search", "code", "translate"] {
        let matches = registry.query(cap);
        if matches.is_empty() {
            println!("Capability '{}': no agents found", cap);
        } else {
            println!("Capability '{}': {:?}", cap, matches);
        }
    }
}
