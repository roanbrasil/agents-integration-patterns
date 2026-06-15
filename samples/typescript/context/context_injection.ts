import { ChatAnthropic } from "@langchain/anthropic";
const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });
const resources = new Map<string, string>([
  ["userProfile", JSON.stringify({ name: "Alice", role: "engineer", team: "platform" })],
  ["document", "The platform team owns CI/CD pipelines and infrastructure automation."],
]);
async function main() {
  const ctx = ["userProfile", "document"].map(k => `${k}: ${resources.get(k)}`).join("\n");
  const prompt = `Use the context below to answer the question.\n\nContext:\n${ctx}\n\nQuestion: What is Alice's team responsible for?`;
  const res = await llm.invoke(prompt);
  console.log("Answer:", res.content as string);
}
main().catch(console.error);
