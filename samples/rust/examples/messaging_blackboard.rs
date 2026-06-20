// Pattern: Blackboard
// Shared state where agents write results; controller reads assembled state.
use aip_samples::FakeAgent;
use std::collections::HashMap;

fn main() {
    println!("=== Blackboard Pattern ===");

    let mut blackboard: HashMap<String, String> = HashMap::new();

    let agents = vec![
        FakeAgent::new("DataFetcher"),
        FakeAgent::new("Analyzer"),
        FakeAgent::new("Formatter"),
    ];
    let keys = vec!["raw_data", "analysis", "formatted_output"];
    let prompts = vec![
        "Fetch sensor readings from API",
        "Analyze the raw_data on the blackboard",
        "Format the analysis result for display",
    ];

    // Each agent writes its result to its own key
    for ((agent, key), prompt) in agents.iter().zip(keys.iter()).zip(prompts.iter()) {
        let result = agent.invoke(prompt);
        blackboard.insert(key.to_string(), result.clone());
        println!("{} wrote [{}]: {}", agent.name, key, result);
    }

    // Controller reads all keys and prints assembled state
    println!("\n--- Controller assembles blackboard state ---");
    let controller = FakeAgent::new("Controller");
    for key in &keys {
        let val = blackboard.get(*key).map(String::as_str).unwrap_or("(empty)");
        let summary = controller.invoke(&format!("Review {}: {}", key, val));
        println!("{}", summary);
    }
}
