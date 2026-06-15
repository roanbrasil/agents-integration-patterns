import { ChatAnthropic } from "@langchain/anthropic";

const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });

async function runJudge(aspect: string, task: string, output: string): Promise<string> {
  const prompt = `You are a ${aspect} judge. Evaluate the output for the given task.\nTask: ${task}\nOutput: ${output}\nReply with exactly APPROVED or REJECTED and one sentence reason.`;
  const res = await llm.invoke(prompt);
  return res.content as string;
}

async function main() {
  const task = "Summarize the benefits of exercise in two sentences.";
  const output = await (async () => {
    const res = await llm.invoke(`Task: ${task}`);
    return res.content as string;
  })();

  console.log("Output to evaluate:\n", output, "\n");

  const [correctness, safety, relevance] = await Promise.all([
    runJudge("correctness", task, output),
    runJudge("safety", task, output),
    runJudge("relevance", task, output),
  ]);

  const verdicts = { correctness, safety, relevance };
  let approvedCount = 0;

  for (const [aspect, verdict] of Object.entries(verdicts)) {
    const passed = verdict.startsWith("APPROVED");
    console.log(`[${aspect.toUpperCase()}] ${verdict}`);
    if (passed) approvedCount++;
  }

  const finalDecision = approvedCount >= 2 ? "APPROVED" : "REJECTED";
  console.log(`\nEnsemble vote: ${approvedCount}/3 approved`);
  console.log(`Final decision: ${finalDecision}`);
}

main().catch(console.error);
