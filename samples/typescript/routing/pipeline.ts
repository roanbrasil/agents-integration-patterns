import { ChatAnthropic } from "@langchain/anthropic";
import { StateGraph, END, START, Annotation } from "@langchain/langgraph";
const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });
const State = Annotation.Root({
  task: Annotation<string>(),
  plan: Annotation<string>(),
  result: Annotation<string>(),
  verified: Annotation<string>(),
});
type S = typeof State.State;
const planner = async (s: S): Promise<Partial<S>> => {
  const r = await llm.invoke(`Create a 3-step plan for: ${s.task}`);
  return { plan: r.content as string };
};
const executor = async (s: S): Promise<Partial<S>> => {
  const r = await llm.invoke(`Execute this plan and show results:\n${s.plan}`);
  return { result: r.content as string };
};
const verifier = async (s: S): Promise<Partial<S>> => {
  const r = await llm.invoke(`Review: does this result address the task?\nTask: ${s.task}\nResult: ${s.result}\nReply PASS or FAIL with reason.`);
  return { verified: r.content as string };
};
const graph = new StateGraph(State)
  .addNode("planner", planner)
  .addNode("executor", executor)
  .addNode("verifier", verifier)
  .addEdge(START, "planner")
  .addEdge("planner", "executor")
  .addEdge("executor", "verifier")
  .addEdge("verifier", END)
  .compile();
async function main() {
  const r = await graph.invoke({ task: "Write a Python function to sort a list of dicts by a key", plan: "", result: "", verified: "" });
  console.log("Plan:", r.plan.substring(0, 100));
  console.log("Result:", r.result.substring(0, 100));
  console.log("Verified:", r.verified);
}
main().catch(console.error);
