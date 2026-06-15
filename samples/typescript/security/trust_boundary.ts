import { ChatAnthropic } from "@langchain/anthropic";
const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });
type TrustLevel = "UNTRUSTED" | "GATEWAY" | "INTERNAL";
async function forward(request: string, level: TrustLevel): Promise<string> {
  if (level === "UNTRUSTED") throw new Error("Access denied: UNTRUSTED caller rejected at boundary");
  const r = await llm.invoke(`[Internal Agent] Process this request: ${request}`);
  return r.content as string;
}
async function main() {
  console.log("=== Trust Boundary ===");
  for (const level of ["UNTRUSTED", "GATEWAY", "INTERNAL"] as TrustLevel[]) {
    try {
      const result = await forward("Get system status", level);
      console.log(`[${level}] OK: ${result.substring(0, 60)}`);
    } catch (e: any) {
      console.log(`[${level}] BLOCKED: ${e.message}`);
    }
  }
}
main().catch(console.error);
