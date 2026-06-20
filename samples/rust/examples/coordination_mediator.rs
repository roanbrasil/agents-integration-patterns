// Pattern: Mediator
// Mediator routes messages between agents without direct coupling.
use aip_samples::FakeAgent;

struct Mediator {
    agent_a: FakeAgent,
    agent_b: FakeAgent,
}

impl Mediator {
    fn new() -> Self {
        Self {
            agent_a: FakeAgent::new("AgentA"),
            agent_b: FakeAgent::new("AgentB"),
        }
    }

    fn mediate(&self, messages: &[(String, String)]) {
        for (sender, message) in messages {
            if sender == "AgentA" {
                // Route A's message to B
                let response = self.agent_b.invoke(&format!("From A: {}", message));
                println!("Mediator: A -> B | msg='{}' | B says: {}", message, response);
            } else if sender == "AgentB" {
                // Route B's message to A
                let response = self.agent_a.invoke(&format!("From B: {}", message));
                println!("Mediator: B -> A | msg='{}' | A says: {}", message, response);
            }
        }
    }
}

fn main() {
    println!("=== Mediator Pattern ===\n");

    let mediator = Mediator::new();

    let messages: Vec<(String, String)> = vec![
        ("AgentA".to_string(), "Request: analyse dataset X".to_string()),
        ("AgentB".to_string(), "Result: 3 anomalies found in dataset X".to_string()),
        ("AgentA".to_string(), "Follow-up: explain anomaly #2".to_string()),
        ("AgentB".to_string(), "Anomaly #2 is a data spike on day 14".to_string()),
    ];

    mediator.mediate(&messages);
}
