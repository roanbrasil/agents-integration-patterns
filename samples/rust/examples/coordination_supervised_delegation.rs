// Pattern: Supervised Delegation
// Supervisor delegates to Worker; validates result; retries once if invalid.
use aip_samples::FakeAgent;

struct Supervisor {
    agent: FakeAgent,
    worker: FakeAgent,
}

impl Supervisor {
    fn new() -> Self {
        Self {
            agent:  FakeAgent::new("Supervisor"),
            worker: FakeAgent::new("Worker"),
        }
    }

    fn delegate(&self, task: &str) -> String {
        let mut result = self.worker.invoke(task);
        println!("Supervisor: delegated task to Worker.");
        println!("Worker result: {}", result);

        if result.trim().is_empty() {
            println!("Supervisor: result invalid — retrying once.");
            result = self.worker.invoke(&format!("[RETRY] {}", task));
            println!("Worker retry result: {}", result);
        }

        let decision = self.agent.invoke(&format!("Validate and approve: {}", result));
        println!("Supervisor decision: {}", decision);
        decision
    }
}

fn main() {
    println!("=== SupervisedDelegation Pattern ===\n");

    let supervisor = Supervisor::new();
    let outcome = supervisor.delegate("Generate a compliance report for Q4");
    println!("\nFinal outcome: {}", outcome);
}
