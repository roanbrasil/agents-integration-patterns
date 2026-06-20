// Pattern: Checkpoint & Resume
// Agent saves progress; on crash, resumes from last checkpoint.
use std::collections::HashMap;

struct Checkpoint {
    step: usize,
    state: String,
}

fn load_checkpoint(store: &HashMap<&str, Checkpoint>) -> Option<&Checkpoint> {
    store.get("main")
}

fn save_checkpoint<'a>(store: &mut HashMap<&'a str, Checkpoint>, step: usize, state: &str) {
    store.insert("main", Checkpoint { step, state: state.to_string() });
}

fn process_step(step: usize, prev_state: &str) -> String {
    format!("output-of-step{}-after-[{}]", step, prev_state)
}

fn main() {
    println!("=== CheckpointResume Pattern ===\n");

    let steps = 4usize;
    let mut checkpoint_store: HashMap<&str, Checkpoint> = HashMap::new();

    // Simulate a crash after step 2: pre-populate checkpoint
    save_checkpoint(&mut checkpoint_store, 2, "state-after-step2");
    println!("Simulated crash: checkpoint saved at step 2.\n");

    // Determine resume point
    let start_step = load_checkpoint(&checkpoint_store)
        .map(|c| c.step)
        .unwrap_or(0);
    let initial_state = load_checkpoint(&checkpoint_store)
        .map(|c| c.state.clone())
        .unwrap_or_default();

    println!("Resuming from step {} (state='{}')\n", start_step, initial_state);

    let mut state = initial_state;
    for step in 0..steps {
        if step < start_step {
            println!("[SKIP] Step {} (already completed)", step);
        } else {
            state = process_step(step, &state);
            save_checkpoint(&mut checkpoint_store, step + 1, &state);
            println!("[EXEC] Step {} -> state='{}'", step, state);
        }
    }

    println!("\nAll {} steps complete. Final state: '{}'", steps, state);
}
