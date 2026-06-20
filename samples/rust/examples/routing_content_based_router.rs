// Pattern: Content-Based Router
// Routes tasks to specialised agents based on keyword inspection.
use aip_samples::FakeAgent;

fn route(task: &str) -> FakeAgent {
    if task.contains("code") || task.contains("debug") {
        FakeAgent::new("CodeAgent")
    } else if task.contains("research") || task.contains("study") {
        FakeAgent::new("ResearchAgent")
    } else {
        FakeAgent::new("GeneralAgent")
    }
}

fn main() {
    println!("=== ContentBasedRouter Pattern ===");

    let tasks = vec![
        "Please code a binary search function",
        "research the history of the Roman Empire",
        "What is the weather like today?",
        "debug the memory leak in the service",
    ];

    for task in &tasks {
        let agent = route(task);
        let result = agent.invoke(task);
        println!("Task: '{}'\n  -> Routed to {}: {}\n", task, agent.name, result);
    }
}
