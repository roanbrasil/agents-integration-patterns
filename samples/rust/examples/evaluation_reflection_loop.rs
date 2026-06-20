// Pattern: Reflection Loop
// Generator produces drafts; Critic checks for required phrase; loop until convergence.

const REQUIRED_PHRASE: &str = "executive summary";
const MAX_ITERATIONS: usize = 3;

// Hardcoded drafts to simulate iterative improvement
fn generate_draft(iteration: usize) -> String {
    match iteration {
        0 => "Here is the quarterly analysis. Revenue grew 12%.".to_string(),
        1 => "Quarterly analysis: Revenue grew 12%. Key highlights are presented below.".to_string(),
        _ => "Executive summary: Revenue grew 12%. Key highlights follow. Recommendation: invest.".to_string(),
    }
}

fn criticize(draft: &str) -> Option<String> {
    if draft.to_lowercase().contains(REQUIRED_PHRASE) {
        None // No feedback needed — draft is acceptable
    } else {
        Some(format!("Draft must include an '{}' section.", REQUIRED_PHRASE))
    }
}

fn main() {
    println!("=== ReflectionLoop Pattern ===\n");
    println!("Required phrase: '{}'\n", REQUIRED_PHRASE);

    let mut final_draft = String::new();

    for iteration in 0..MAX_ITERATIONS {
        let draft = generate_draft(iteration);
        println!("Iteration {}: Generator produced:", iteration + 1);
        println!("  \"{}\"", draft);

        match criticize(&draft) {
            None => {
                println!("  Critic: APPROVED — no issues found.");
                final_draft = draft;
                break;
            }
            Some(feedback) => {
                println!("  Critic: FEEDBACK — {}", feedback);
                final_draft = draft;
            }
        }
        println!();
    }

    println!("\nFinal draft: \"{}\"", final_draft);
}
