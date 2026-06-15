import { ChatAnthropic } from "@langchain/anthropic";
const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });
async function route(task: string) {
  const cat = (await llm.invoke(`Classify into one word: "coding", "research", or "data". Task: ${task}. Respond with one word only.`)).content as string;
  const label = cat.toLowerCase().includes("cod") ? "coding" : cat.toLowerCase().includes("res") ? "research" : "data";
  const specialist = await llm.invoke(`You are a ${label} specialist. Answer briefly: ${task}`);
  console.log(`[${label}] ${task.substring(0, 40)}: ${(specialist.content as string).substring(0, 80)}`);
}
async function main() {
  await route("How do I reverse a linked list in Python?");
  await route("What caused World War I?");
  await route("What is the average of [4, 8, 15, 16, 23, 42]?");
}
main().catch(console.error);
