// Pattern: Agent Proxy
// Proxy wraps a backend agent, translating requests transparently.
use aip_samples::FakeAgent;

struct AgentProxy {
    backend: FakeAgent,
}

impl AgentProxy {
    fn new(backend: FakeAgent) -> Self { Self { backend } }

    fn invoke(&self, prompt: &str) -> String {
        // Protocol translation: uppercase the prompt before forwarding
        let translated = prompt.to_uppercase();
        println!("Proxy translates: '{}' -> '{}'", prompt, translated);
        self.backend.invoke(&translated)
    }
}

fn main() {
    println!("=== AgentProxy Pattern ===");

    let backend = FakeAgent::new("BackendAgent");
    let proxy = AgentProxy::new(backend);

    let result = proxy.invoke("please analyse the quarterly report");
    println!("Caller receives: {}", result);
}
