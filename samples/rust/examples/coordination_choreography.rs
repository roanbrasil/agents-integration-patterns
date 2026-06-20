// Pattern: Choreography
// Agents react to a shared event log without a central coordinator.
use aip_samples::FakeAgent;

fn main() {
    println!("=== Choreography Pattern ===\n");

    let agents = vec![
        FakeAgent::new("InventoryAgent"),
        FakeAgent::new("PaymentAgent"),
        FakeAgent::new("ShippingAgent"),
    ];

    let triggers = vec![
        "OrderPlaced: order_id=42, item=Widget",
        "PaymentReceived: order_id=42, amount=$99",
        "ReadyToShip: order_id=42",
    ];

    let mut event_log: Vec<String> = Vec::new();

    for (agent, trigger) in agents.iter().zip(triggers.iter()) {
        // Agent reacts to latest event in log (if any)
        if let Some(last_event) = event_log.last() {
            println!("{} reacts to: {}", agent.name, last_event);
        }

        // Agent emits its own event
        let event = agent.invoke(trigger);
        event_log.push(event.clone());
        println!("{} emits: {}\n", agent.name, event);
    }

    println!("--- Full event log ---");
    for (i, ev) in event_log.iter().enumerate() {
        println!("  [{}] {}", i + 1, ev);
    }
}
