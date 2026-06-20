// Pattern: Saga
// Distributed transaction with compensations on failure.

struct SagaStep {
    name: &'static str,
    execute: fn() -> Result<String, String>,
    compensate: fn() -> String,
}

fn step1_execute()    -> Result<String, String> { Ok("Step1: ReserveInventory done".to_string()) }
fn step1_compensate() -> String                  { "Step1: ReleaseInventory".to_string() }

fn step2_execute()    -> Result<String, String> { Err("Step2: ChargeCreditCard FAILED — insufficient funds".to_string()) }
fn step2_compensate() -> String                  { "Step2: RefundCreditCard".to_string() }

fn step3_execute()    -> Result<String, String> { Ok("Step3: ShipOrder done".to_string()) }
fn step3_compensate() -> String                  { "Step3: CancelShipment".to_string() }

fn main() {
    println!("=== Saga Pattern ===\n");

    let steps: Vec<SagaStep> = vec![
        SagaStep { name: "ReserveInventory", execute: step1_execute, compensate: step1_compensate },
        SagaStep { name: "ChargeCreditCard", execute: step2_execute, compensate: step2_compensate },
        SagaStep { name: "ShipOrder",        execute: step3_execute, compensate: step3_compensate },
    ];

    let mut completed: Vec<&SagaStep> = Vec::new();
    let mut saga_log: Vec<String> = Vec::new();

    for step in &steps {
        match (step.execute)() {
            Ok(msg) => {
                println!("[OK]   [{}] {}", step.name, msg);
                saga_log.push(format!("EXECUTE {}", msg));
                completed.push(step);
            }
            Err(err) => {
                println!("[FAIL] [{}] {}", step.name, err);
                saga_log.push(format!("FAILED {}", err));
                // Compensate in reverse order
                println!("\nStarting compensations...");
                for done_step in completed.iter().rev() {
                    let comp = (done_step.compensate)();
                    println!("[COMP] {}", comp);
                    saga_log.push(format!("COMPENSATE {}", comp));
                }
                break;
            }
        }
    }

    println!("\n--- Saga Log ---");
    for entry in &saga_log {
        println!("  {}", entry);
    }
}
