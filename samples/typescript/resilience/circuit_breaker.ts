type CBState = "CLOSED" | "OPEN" | "HALF_OPEN";
class CircuitBreaker {
  private failures = 0;
  private state: CBState = "CLOSED";
  private openedAt = 0;
  constructor(private threshold = 3, private timeout = 100) {}
  async call<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === "OPEN") {
      if (Date.now() - this.openedAt >= this.timeout) { this.state = "HALF_OPEN"; }
      else throw new Error(`[CB] OPEN — blocking call`);
    }
    try {
      const r = await fn();
      this.failures = 0; this.state = "CLOSED";
      return r;
    } catch (e) {
      this.failures++;
      if (this.failures >= this.threshold) { this.state = "OPEN"; this.openedAt = Date.now(); }
      throw e;
    }
  }
  getState() { return this.state; }
}
let callCount = 0;
async function flaky(): Promise<string> {
  callCount++;
  if (callCount <= 3) throw new Error(`Downstream fail #${callCount}`);
  return `[LLM] answer on call #${callCount}`;
}
async function main() {
  const cb = new CircuitBreaker(3, 100);
  for (let i = 1; i <= 7; i++) {
    try {
      const r = await cb.call(flaky);
      console.log(`Attempt ${i} [${cb.getState()}]: ${r}`);
    } catch (e: any) {
      console.log(`Attempt ${i} [${cb.getState()}]: ${e.message}`);
    }
    if (i === 4) await new Promise(r => setTimeout(r, 150));
  }
}
main().catch(console.error);
