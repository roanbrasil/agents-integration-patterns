// Pattern: LLM-as-Judge
// A judge evaluates output against a rubric of required keywords.

#[derive(Debug)]
enum Verdict {
    Approved,
    Rejected(String),
}

struct Judge {
    name: String,
    required_keywords: Vec<String>,
}

impl Judge {
    fn new(name: &str, required_keywords: Vec<&str>) -> Self {
        Self {
            name: name.to_string(),
            required_keywords: required_keywords.iter().map(|s| s.to_string()).collect(),
        }
    }

    fn evaluate(&self, output: &str) -> Verdict {
        let lower = output.to_lowercase();
        let missing: Vec<&str> = self.required_keywords
            .iter()
            .filter(|kw| !lower.contains(kw.as_str()))
            .map(String::as_str)
            .collect();

        if missing.is_empty() {
            Verdict::Approved
        } else {
            Verdict::Rejected(format!("missing required keywords: {:?}", missing))
        }
    }
}

fn main() {
    println!("=== LLM-as-Judge Pattern ===\n");

    let judge = Judge::new("QualityJudge", vec!["conclusion", "evidence", "recommendation"]);

    let outputs = vec![
        ("Good output",
         "The evidence clearly supports our conclusion. Our recommendation is to proceed."),
        ("Incomplete output",
         "We looked at the data and found some interesting patterns."),
        ("Partial output",
         "The evidence is strong and leads to an important conclusion."),
    ];

    for (label, output) in &outputs {
        let verdict = judge.evaluate(output);
        match &verdict {
            Verdict::Approved        => println!("[{}] {} -> APPROVED", judge.name, label),
            Verdict::Rejected(reason) => println!("[{}] {} -> REJECTED: {}", judge.name, label, reason),
        }
        println!("  Output: \"{}\"\n", output);
    }
}
