// Pattern: Trust Boundary
// Messages crossing trust tiers must pass validation; violations are blocked.

#[derive(Debug, Clone, PartialEq, PartialOrd)]
enum TrustTier { Untrusted = 0, Gateway = 1, Trusted = 2 }

fn validate_crossing(from: &TrustTier, to: &TrustTier) -> bool {
    // Only allow crossing to the immediately next tier or same tier
    (*to as i32) - (*from as i32) <= 1
}

struct Message {
    content: String,
    from_tier: TrustTier,
    to_tier: TrustTier,
}

fn route(msg: &Message) -> Result<String, String> {
    if validate_crossing(&msg.from_tier, &msg.to_tier) {
        Ok(format!("Delivered '{}' ({:?} -> {:?})", msg.content, msg.from_tier, msg.to_tier))
    } else {
        Err(format!("BLOCKED '{}' ({:?} -> {:?}): trust boundary violation",
            msg.content, msg.from_tier, msg.to_tier))
    }
}

fn main() {
    println!("=== TrustBoundary Pattern ===\n");

    let messages = vec![
        Message { content: "Login request".to_string(),
                  from_tier: TrustTier::Untrusted, to_tier: TrustTier::Gateway },
        Message { content: "Authenticated API call".to_string(),
                  from_tier: TrustTier::Gateway,   to_tier: TrustTier::Trusted },
        Message { content: "Direct internal access".to_string(),
                  from_tier: TrustTier::Untrusted, to_tier: TrustTier::Trusted },
        Message { content: "Internal service call".to_string(),
                  from_tier: TrustTier::Trusted,   to_tier: TrustTier::Trusted },
    ];

    for msg in &messages {
        match route(msg) {
            Ok(r)  => println!("[ALLOW] {}", r),
            Err(e) => println!("[BLOCK] {}", e),
        }
    }
}
