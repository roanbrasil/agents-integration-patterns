import { ChatAnthropic } from "@langchain/anthropic";
import { StateGraph, END, START, Annotation } from "@langchain/langgraph";
import { MemorySaver } from "@langchain/langgraph";
const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });
const State = Annotation.Root({
  step: Annotation<number>(),
  results: Annotation<string[]>({ reducer: (a, b) => [...a, ...b], default: () => [] }),
});
type S = typeof State.State;
const step1 = async (s: S): Promise<Partial<S>> => {
  const r = await llm.invoke("Step 1: List 2 benefits of microservices.");
  console.log("Checkpoint after step 1");
  return { step: 2, results: [r.content as string] };
};
const step2 = async (s: S): Promise<Partial<S>> => {
  const r = await llm.invoke("Step 2: List 2 drawbacks of microservices.");
  console.log("Checkpoint after step 2");
  return { step: 3, results: [r.content as string] };
};
const step3 = async (s: S): Promise<Partial<S>> => {
  const r = await llm.invoke("Step 3: Give a one-sentence verdict on microservices.");
  console.log("Checkpoint after step 3");
  return { step: 4, results: [r.content as string] };
};
const checkpointer = new MemorySaver();
const graph = new StateGraph(State)
  .addNode("step1", step1).addNode("step2", step2).addNode("step3", step3)
  .addEdge(START, "step1").addEdge("step1", "step2").addEdge("step2", "step3").addEdge("step3", END)
  .compile({ checkpointer });
async function main() {
  const config = { configurable: { thread_id: "microservices-analysis" } };
  const r = await graph.invoke({ step: 1, results: [] }, config);
  console.log("All results:", r.results.length, "steps completed");
  r.results.forEach((res, i) => console.log(`Step ${i+1}:`, (res as string).substring(0, 60)));
}
main().catch(console.error);
