// Pattern: Circuit Breaker
// Protects downstream calls; opens on repeated failures, probes for recovery.
use std::time::{Duration, Instant};

#[derive(Debug, PartialEq)]
enum State { Closed, Open, HalfOpen }

struct CircuitBreaker {
    state: State,
    failure_count: u32,
    failure_threshold: u32,
    recovery_timeout: Duration,
    opened_at: Option<Instant>,
}

impl CircuitBreaker {
    fn new(failure_threshold: u32, recovery_timeout_ms: u64) -> Self {
        Self {
            state: State::Closed,
            failure_count: 0,
            failure_threshold,
            recovery_timeout: Duration::from_millis(recovery_timeout_ms),
            opened_at: None,
        }
    }

    fn call(&mut self, name: &str, success: bool) -> Result<String, String> {
        // Check if we should transition from Open to HalfOpen
        if self.state == State::Open {
            if let Some(opened_at) = self.opened_at {
                if opened_at.elapsed() >= self.recovery_timeout {
                    self.state = State::HalfOpen;
                    println!("CircuitBreaker: OPEN -> HALF_OPEN (probe allowed)");
                }
            }
        }

        match self.state {
            State::Open => Err(format!("{}: circuit OPEN — call rejected", name)),
            State::Closed | State::HalfOpen => {
                if success {
                    self.failure_count = 0;
                    self.state = State::Closed;
                    println!("CircuitBreaker: call OK (state=CLOSED)");
                    Ok(format!("{}: success", name))
                } else {
                    self.failure_count += 1;
                    println!("CircuitBreaker: call FAILED (failures={})", self.failure_count);
                    if self.failure_count >= self.failure_threshold {
                        self.state = State::Open;
                        self.opened_at = Some(Instant::now());
                        println!("CircuitBreaker: CLOSED -> OPEN");
                    }
                    Err(format!("{}: failure", name))
                }
            }
        }
    }
}

fn main() {
    println!("=== CircuitBreaker Pattern ===\n");

    let mut cb = CircuitBreaker::new(3, 50);

    // Simulate 3 failures -> circuit opens
    for i in 1..=3 {
        let r = cb.call(&format!("call-{}", i), false);
        println!("Result: {:?}\n", r);
    }

    // Call rejected while OPEN
    let r = cb.call("call-4", true);
    println!("Result (should be rejected): {:?}\n", r);

    // Wait for recovery timeout
    std::thread::sleep(Duration::from_millis(60));

    // Probe in HALF_OPEN succeeds -> circuit closes
    let r = cb.call("call-5", true);
    println!("Result (probe): {:?}", r);
    println!("Final state: {:?}", cb.state);
}
