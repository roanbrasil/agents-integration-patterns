// Pattern: Broker
// Broker routes tasks to the best provider based on capability and score.
use aip_samples::FakeAgent;

struct Provider {
    name: String,
    capability: String,
    score: f32,
}

struct Broker {
    providers: Vec<Provider>,
}

impl Broker {
    fn new() -> Self { Self { providers: Vec::new() } }

    fn register(&mut self, name: &str, capability: &str, score: f32) {
        self.providers.push(Provider {
            name: name.to_string(),
            capability: capability.to_string(),
            score,
        });
    }

    fn route(&self, task: &str) -> Option<&Provider> {
        self.providers
            .iter()
            .filter(|p| task.contains(&p.capability))
            .max_by(|a, b| a.score.partial_cmp(&b.score).unwrap())
    }
}

fn main() {
    println!("=== Broker Pattern ===");

    let mut broker = Broker::new();
    broker.register("ResearchPro",  "research", 0.9);
    broker.register("ResearchLite", "research", 0.6);
    broker.register("CodeMaster",   "code",     0.95);

    let tasks = vec![
        "research the latest AI trends",
        "code a sorting algorithm",
        "translate a document",
    ];

    for task in &tasks {
        match broker.route(task) {
            Some(provider) => {
                let agent = FakeAgent::new(&provider.name);
                let result = agent.invoke(task);
                println!("Task: '{}'\n  -> Routed to {} (score={:.1}): {}\n",
                    task, provider.name, provider.score, result);
            }
            None => println!("Task: '{}'\n  -> No provider found\n", task),
        }
    }
}
