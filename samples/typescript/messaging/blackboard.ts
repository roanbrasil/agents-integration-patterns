import { ChatAnthropic } from "@langchain/anthropic";

const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });

const blackboard = new Map<string, string>();

async function agentA(): Promise<void> {
  const res = await llm.invoke("State a complex logical puzzle in 2 sentences.");
  blackboard.set("problem", res.content as string);
  console.log("AgentA wrote problem:", blackboard.get("problem"));
}

async function agentB(): Promise<void> {
  const problem = blackboard.get("problem") ?? "";
  const res = await llm.invoke(
    `Given this puzzle: "${problem}" — provide a partial analysis, not the full answer.`
  );
  blackboard.set("partial_solution", res.content as string);
  console.log("\nAgentB wrote partial solution:", blackboard.get("partial_solution"));
}

async function agentC(): Promise<void> {
  const problem = blackboard.get("problem") ?? "";
  const partial = blackboard.get("partial_solution") ?? "";
  const res = await llm.invoke(
    `Problem: "${problem}"\nPartial analysis: "${partial}"\nProvide a final conclusion.`
  );
  blackboard.set("conclusion", res.content as string);
  console.log("\nAgentC wrote conclusion:", blackboard.get("conclusion"));
}

async function main() {
  await agentA();
  await agentB();
  await agentC();
  console.log("\nFinal Blackboard State:");
  blackboard.forEach((value, key) => console.log(`  ${key}: ${value}`));
}

main().catch(console.error);
