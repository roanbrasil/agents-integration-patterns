// Pattern: Broadcast Message
// Publisher sends a message to multiple subscriber agents independently.
use aip_samples::FakeAgent;

fn main() {
    println!("=== BroadcastMessage Pattern ===");

    let publisher = FakeAgent::new("Publisher");
    let subscribers: Vec<FakeAgent> = vec![
        FakeAgent::new("ResearchAgent"),
        FakeAgent::new("AnalysisAgent"),
        FakeAgent::new("SummaryAgent"),
    ];

    let message = publisher.invoke("New market data available: Q4 earnings report released.");
    println!("Publisher broadcasts: {}\n", message);

    for sub in &subscribers {
        let response = sub.invoke(&format!("Process broadcast: {}", message));
        println!("{} processed: {}", sub.name, response);
    }
}
