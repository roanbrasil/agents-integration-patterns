// Pattern: Peer-to-Peer Delegation
// Agent A delegates math to B; Agent B delegates language to C.
use aip_samples::FakeAgent;

struct AgentA { agent: FakeAgent }
struct AgentB { agent: FakeAgent }
struct AgentC { agent: FakeAgent }

impl AgentA {
    fn handle(&self, task: &str, b: &AgentB) -> String {
        if task.contains("math") || task.contains("calculate") {
            println!("{}: can't handle math — delegating to AgentB.", self.agent.name);
            b.handle(task, &AgentC { agent: FakeAgent::new("AgentC") })
        } else {
            self.agent.invoke(task)
        }
    }
}

impl AgentB {
    fn handle(&self, task: &str, c: &AgentC) -> String {
        if task.contains("language") || task.contains("translate") {
            println!("{}: can't handle language — delegating to AgentC.", self.agent.name);
            c.handle(task)
        } else {
            self.agent.invoke(task)
        }
    }
}

impl AgentC {
    fn handle(&self, task: &str) -> String {
        self.agent.invoke(task)
    }
}

fn main() {
    println!("=== PeerToPeerDelegation Pattern ===\n");

    let a = AgentA { agent: FakeAgent::new("AgentA") };
    let b = AgentB { agent: FakeAgent::new("AgentB") };
    let c = AgentC { agent: FakeAgent::new("AgentC") };

    let tasks = vec![
        "calculate the integral of x^2",
        "translate this sentence to French",
        "summarise this document",
    ];

    for task in &tasks {
        println!("Task: '{}'", task);
        let result = a.handle(task, &b);
        let _ = c; // may be unused for non-delegating tasks
        println!("Result: {}\n", result);
    }
}
