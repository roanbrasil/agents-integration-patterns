// Pattern: Ensemble Judge
// Multiple judges vote; majority (>=2) determines final verdict.

#[derive(Debug, Clone, PartialEq)]
enum Vote { Approved, Rejected(String) }

struct LensJudge {
    name: String,
    required_keyword: String,
}

impl LensJudge {
    fn new(name: &str, keyword: &str) -> Self {
        Self { name: name.to_string(), required_keyword: keyword.to_string() }
    }

    fn vote(&self, output: &str) -> Vote {
        if output.to_lowercase().contains(&self.required_keyword) {
            Vote::Approved
        } else {
            Vote::Rejected(format!("missing '{}'", self.required_keyword))
        }
    }
}

fn main() {
    println!("=== EnsembleJudge Pattern ===\n");

    let judges = vec![
        LensJudge::new("CorrectnessJudge", "accurate"),
        LensJudge::new("SafetyJudge",      "safe"),
        LensJudge::new("RelevanceJudge",   "relevant"),
    ];

    let outputs = vec![
        "This is an accurate and relevant response that is safe to share.",
        "This is accurate but may not be relevant to the user's query.",
        "This response is problematic and inaccurate.",
    ];

    for output in &outputs {
        println!("Output: \"{}\"", output);
        let votes: Vec<(&str, Vote)> = judges
            .iter()
            .map(|j| (j.name.as_str(), j.vote(output)))
            .collect();

        let approved_count = votes.iter().filter(|(_, v)| *v == Vote::Approved).count();
        for (name, vote) in &votes {
            match vote {
                Vote::Approved       => println!("  {} -> APPROVED", name),
                Vote::Rejected(r)    => println!("  {} -> REJECTED ({})", name, r),
            }
        }

        let final_verdict = if approved_count >= 2 { "APPROVED" } else { "REJECTED" };
        println!("  Final ({}/{} approved): {}\n", approved_count, judges.len(), final_verdict);
    }
}
