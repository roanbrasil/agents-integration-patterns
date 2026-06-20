// Pattern: Orchestrator
// Orchestrator runs worker agents sequentially, passing shared state between steps.
use aip_samples::FakeAgent;
use std::collections::HashMap;

struct WorkerAgent {
    step_name: String,
    agent: FakeAgent,
}

struct Orchestrator {
    workers: Vec<WorkerAgent>,
}

impl Orchestrator {
    fn new() -> Self { Self { workers: Vec::new() } }

    fn add_worker(&mut self, step_name: &str, agent_name: &str) {
        self.workers.push(WorkerAgent {
            step_name: step_name.to_string(),
            agent: FakeAgent::new(agent_name),
        });
    }

    fn run(&self, initial_input: &str) -> HashMap<String, String> {
        let mut state: HashMap<String, String> = HashMap::new();
        state.insert("input".to_string(), initial_input.to_string());

        for worker in &self.workers {
            let prompt = format!("[{}] state={:?}", worker.step_name, state);
            let output = worker.agent.invoke(&prompt);
            println!("Step '{}': {}", worker.step_name, output);
            state.insert(worker.step_name.clone(), output);
        }
        state
    }
}

fn main() {
    println!("=== Orchestrator Pattern ===\n");

    let mut orchestrator = Orchestrator::new();
    orchestrator.add_worker("data_fetch",  "FetchAgent");
    orchestrator.add_worker("data_clean",  "CleanAgent");
    orchestrator.add_worker("data_report", "ReportAgent");

    let final_state = orchestrator.run("raw sales CSV file");
    println!("\nFinal state keys: {:?}", final_state.keys().collect::<Vec<_>>());
}
