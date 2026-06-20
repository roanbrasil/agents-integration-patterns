/// Shared FakeAgent and types for all AIP samples.
/// No real LLM calls — responses are deterministic stubs.

pub struct FakeAgent {
    pub name: String,
}

impl FakeAgent {
    pub fn new(name: &str) -> Self {
        Self { name: name.to_string() }
    }

    pub fn invoke(&self, prompt: &str) -> String {
        let snippet = &prompt[..prompt.len().min(60)];
        format!("[{}] {}", self.name, snippet)
    }

    pub async fn invoke_async(&self, prompt: &str) -> String {
        self.invoke(prompt)
    }
}
