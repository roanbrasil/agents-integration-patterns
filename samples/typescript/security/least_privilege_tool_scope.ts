class ScopedToolServer {
  constructor(private allowed: Set<string>) {}
  callTool(name: string, args: string): string {
    if (!this.allowed.has(name)) throw new Error(`Tool "${name}" out of scope. Allowed: [${[...this.allowed].join(", ")}]`);
    return `[${name}] executed with args: ${args}`;
  }
  listTools(): string[] { return [...this.allowed]; }
}
async function main() {
  const researchServer = new ScopedToolServer(new Set(["search", "read"]));
  const execServer = new ScopedToolServer(new Set(["write", "run"]));
  console.log("=== Least-Privilege Tool Scope ===");
  console.log(researchServer.callTool("search", "AI papers 2025"));
  try { researchServer.callTool("write", "exfiltrate data"); }
  catch (e: any) { console.log("BLOCKED:", e.message); }
  console.log(execServer.callTool("write", "report.txt"));
  try { execServer.callTool("search", "sensitive data"); }
  catch (e: any) { console.log("BLOCKED:", e.message); }
}
main().catch(console.error);
