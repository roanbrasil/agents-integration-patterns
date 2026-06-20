// Pattern: Scatter-Gather
// Fan out one task to multiple agents concurrently, then collect all results.
use aip_samples::FakeAgent;

#[tokio::main]
async fn main() {
    println!("=== ScatterGather Pattern ===");

    let agent_a = FakeAgent::new("AgentAlpha");
    let agent_b = FakeAgent::new("AgentBeta");
    let agent_c = FakeAgent::new("AgentGamma");

    let task = "Analyse the impact of AI on healthcare";
    println!("Scattering task to 3 agents: '{}'\n", task);

    // Fan out concurrently
    let (r1, r2, r3) = tokio::join!(
        agent_a.invoke_async(task),
        agent_b.invoke_async(task),
        agent_c.invoke_async(task),
    );

    let results: Vec<String> = vec![r1, r2, r3];

    println!("Gathered results:");
    for (i, r) in results.iter().enumerate() {
        println!("  [{}] {}", i + 1, r);
    }

    println!("\nAll {} results gathered successfully.", results.len());
}
