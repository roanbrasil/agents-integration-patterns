// Pattern: Dead Letter Agent
// Tasks that fail max_retries times are moved to a dead-letter queue.
use aip_samples::FakeAgent;

fn try_process(agent: &FakeAgent, task: &str, attempt: u32) -> Result<String, String> {
    // Simulate tasks containing "poison" always fail
    if task.contains("poison") {
        Err(format!("Processing failed on attempt {}", attempt))
    } else {
        Ok(agent.invoke(task))
    }
}

fn main() {
    println!("=== DeadLetterAgent Pattern ===\n");

    let agent = FakeAgent::new("WorkerAgent");
    let max_retries = 3u32;

    let queue: Vec<&str> = vec![
        "Summarise report A",
        "poison: invalid payload",
        "Analyse dataset B",
        "poison: corrupt message",
        "Generate invoice C",
    ];

    let mut dlq: Vec<String> = Vec::new();

    for task in &queue {
        let mut success = false;
        for attempt in 1..=max_retries {
            match try_process(&agent, task, attempt) {
                Ok(result) => {
                    println!("[OK]  Task '{}' processed: {}", task, result);
                    success = true;
                    break;
                }
                Err(e) => {
                    println!("[ERR] Task '{}' attempt {}/{}: {}", task, attempt, max_retries, e);
                }
            }
        }
        if !success {
            println!("[DLQ] Task '{}' escalated to dead-letter queue.\n", task);
            dlq.push(task.to_string());
        } else {
            println!();
        }
    }

    println!("--- Dead Letter Queue ({} items) ---", dlq.len());
    for item in &dlq {
        println!("  {}", item);
    }
}
