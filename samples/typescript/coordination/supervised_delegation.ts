import { ChatAnthropic } from "@langchain/anthropic";
const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });
async function main() {
  const goal = "Analyze the pros and cons of microservices architecture";
  const split = await llm.invoke(`Split this goal into exactly 2 subtasks (one line each): ${goal}`);
  const subtasks = (split.content as string).split("\n").filter(l => l.trim()).slice(0, 2);
  console.log("Subtasks:", subtasks);
  const [rA, rB] = await Promise.all([
    llm.invoke(`Worker A: ${subtasks[0] ?? goal}`).then(r => r.content as string),
    llm.invoke(`Worker B: ${subtasks[1] ?? goal}`).then(r => r.content as string),
  ]);
  const review = await llm.invoke(`Supervisor: synthesize these worker results in 3 sentences:\nWorker A: ${rA}\nWorker B: ${rB}`);
  console.log("Final review:", review.content as string);
}
main().catch(console.error);
