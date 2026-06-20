// Pattern: Group Chat
// Multiple agents take turns responding to a shared topic; moderator prints transcript.
use aip_samples::FakeAgent;

fn main() {
    println!("=== GroupChat Pattern ===\n");

    let agents = vec![
        FakeAgent::new("Alice"),
        FakeAgent::new("Bob"),
        FakeAgent::new("Carol"),
    ];

    let topic = "How should we approach AI safety in 2025?";
    println!("Topic: {}\n", topic);

    let mut transcript: Vec<(String, String)> = Vec::new();

    for agent in &agents {
        // Each agent responds to the topic (and optionally the prior responses)
        let prompt = if transcript.is_empty() {
            format!("Topic: {}", topic)
        } else {
            let last = &transcript[transcript.len() - 1];
            format!("Topic: {} | Previous: {} said '{}'", topic, last.0, last.1)
        };
        let response = agent.invoke(&prompt);
        println!("{}: {}", agent.name, response);
        transcript.push((agent.name.clone(), response));
    }

    // Moderator prints full transcript
    println!("\n--- Moderator Transcript ---");
    for (name, msg) in &transcript {
        println!("  {}: {}", name, msg);
    }
}
