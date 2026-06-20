// Pattern: Direct Message
// Agent A sends a task to Agent B via a point-to-point channel.
use aip_samples::FakeAgent;

fn main() {
    println!("=== DirectMessage Pattern ===");

    let agent_a = FakeAgent::new("AgentA");
    let agent_b = FakeAgent::new("AgentB");

    // Agent A generates a question
    let question = agent_a.invoke("What is the capital of France?");
    println!("A sends : {}", question);

    // Agent B receives and answers
    let answer = agent_b.invoke(&format!("Answer this: {}", question));
    println!("B replies: {}", answer);
}
