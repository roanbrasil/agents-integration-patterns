// Pattern: Magentic (Ledger-based Orchestration)
// Ledger tracks completed subtasks; orchestrator skips already-done steps.
use aip_samples::FakeAgent;

struct Ledger {
    completed: Vec<String>,
}

impl Ledger {
    fn new() -> Self { Self { completed: Vec::new() } }
    fn is_done(&self, subtask: &str) -> bool { self.completed.contains(&subtask.to_string()) }
    fn mark_done(&mut self, subtask: &str) { self.completed.push(subtask.to_string()); }
}

struct MagenticOrchestrator {
    agent: FakeAgent,
    ledger: Ledger,
}

impl MagenticOrchestrator {
    fn new() -> Self {
        Self {
            agent: FakeAgent::new("MagenticAgent"),
            ledger: Ledger::new(),
        }
    }

    fn run(&mut self, subtasks: &[&str]) {
        for subtask in subtasks {
            if self.ledger.is_done(subtask) {
                println!("[SKIP] '{}' already in ledger — skipping.", subtask);
            } else {
                let result = self.agent.invoke(subtask);
                println!("[EXEC] '{}' -> {}", subtask, result);
                self.ledger.mark_done(subtask);
            }
        }
    }
}

fn main() {
    println!("=== Magentic Pattern ===\n");

    let mut orchestrator = MagenticOrchestrator::new();

    // Pre-seed ledger with a completed step
    orchestrator.ledger.mark_done("FetchData");
    println!("Pre-seeded ledger: FetchData already done.\n");

    let subtasks = vec!["FetchData", "CleanData", "FetchData", "AnalyseData", "GenerateReport"];
    orchestrator.run(&subtasks);

    println!("\nLedger: {:?}", orchestrator.ledger.completed);
}
