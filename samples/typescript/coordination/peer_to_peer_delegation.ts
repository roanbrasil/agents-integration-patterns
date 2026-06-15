import { ChatAnthropic } from "@langchain/anthropic";
const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });
interface AgentCard { name: string; capabilities: string[]; }
const registry: AgentCard[] = [
  { name: "TranslationAgent", capabilities: ["translate", "localize"] },
  { name: "SummaryAgent", capabilities: ["summarize", "condense"] },
  { name: "OCRAgent", capabilities: ["pdf-ocr", "image-text"] },
];
function discover(cap: string): AgentCard | undefined {
  return registry.find(a => a.capabilities.some(c => c.toLowerCase().includes(cap.toLowerCase())));
}
async function main() {
  const needed = "summarize";
  const peer = discover(needed);
  if (!peer) { console.log("No agent found for", needed); return; }
  console.log(`Discovered: ${peer.name} for "${needed}"`);
  const result = await llm.invoke(`You are ${peer.name}. Summarize: The microservices pattern decomposes an app into small independent services.`);
  console.log("Delegated result:", result.content as string);
}
main().catch(console.error);
