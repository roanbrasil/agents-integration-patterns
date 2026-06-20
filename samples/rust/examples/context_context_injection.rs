// Pattern: Context Injection
// ContextAssembler builds a context string from documents injected into agent prompt.
use aip_samples::FakeAgent;

struct ContextAssembler {
    documents: Vec<String>,
}

impl ContextAssembler {
    fn new() -> Self { Self { documents: Vec::new() } }

    fn add_document(&mut self, doc: &str) {
        self.documents.push(doc.to_string());
    }

    fn assemble(&self) -> String {
        self.documents
            .iter()
            .enumerate()
            .map(|(i, d)| format!("[Doc {}] {}", i + 1, d))
            .collect::<Vec<_>>()
            .join("\n")
    }
}

fn main() {
    println!("=== ContextInjection Pattern ===");

    let mut assembler = ContextAssembler::new();
    assembler.add_document("Revenue for Q3 was $4.2M, up 12% YoY.");
    assembler.add_document("Key risks: supply chain disruption and FX headwinds.");
    assembler.add_document("Strategic goal: expand into APAC by Q2 next year.");

    let context = assembler.assemble();
    println!("Assembled context:\n{}\n", context);

    let agent = FakeAgent::new("AnalystAgent");
    let injected_prompt = format!(
        "Using the following context:\n{}\n\nTask: Summarize the key business insights.",
        context
    );
    let response = agent.invoke(&injected_prompt);
    println!("Agent response: {}", response);
}
