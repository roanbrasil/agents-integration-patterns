// Pattern: Idempotent Agent
// Operations with the same ID execute only once; duplicates return cached result.
use std::collections::HashMap;

struct IdempotencyStore {
    cache: HashMap<String, String>,
}

impl IdempotencyStore {
    fn new() -> Self { Self { cache: HashMap::new() } }

    fn execute(&mut self, operation_id: &str, work: impl Fn() -> String) -> (String, bool) {
        if let Some(cached) = self.cache.get(operation_id) {
            return (cached.clone(), false /* was_executed */);
        }
        let result = work();
        self.cache.insert(operation_id.to_string(), result.clone());
        (result, true)
    }
}

fn main() {
    println!("=== IdempotentAgent Pattern ===\n");

    let mut store = IdempotencyStore::new();

    let operations = vec![
        ("op-001", "Send invoice to customer@example.com"),
        ("op-002", "Update user profile record"),
        ("op-001", "Send invoice to customer@example.com"), // duplicate
        ("op-003", "Trigger notification"),
        ("op-002", "Update user profile record"),           // duplicate
    ];

    for (op_id, task) in &operations {
        let (result, executed) = store.execute(op_id, || {
            format!("Executed: {}", task)
        });
        if executed {
            println!("[NEW]  {} -> {}", op_id, result);
        } else {
            println!("[SKIP] {} -> cached: {} (no-op)", op_id, result);
        }
    }

    println!("\nStore has {} unique operations.", store.cache.len());
}
