import { ChatAnthropic } from "@langchain/anthropic";
import { StateGraph, END, START, Annotation } from "@langchain/langgraph";
const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });
const State = Annotation.Root({
  task: Annotation<string>(),
  result: Annotation<string>(),
  error: Annotation<string>(),
  retries: Annotation<number>(),
  status: Annotation<string>(),
});
type S = typeof State.State;
const agentNode = async (s: S): Promise<Partial<S>> => {
  if (s.retries < 1) return { error: "Simulated failure", status: "failed", retries: s.retries + 1 };
  const r = await llm.invoke(`Complete this task: ${s.task}`);
  return { result: r.content as string, status: "done" };
};
const deadLetterNode = async (s: S): Promise<Partial<S>> => {
  console.log(`[DeadLetter] Task failed: ${s.error}`);
  return { status: "dead_letter" };
};
const route = (s: S) => s.status === "done" ? END : s.status === "failed" && s.retries >= 2 ? "deadLetter" : "agent";
const graph = new StateGraph(State)
  .addNode("agent", agentNode).addNode("deadLetter", deadLetterNode)
  .addEdge(START, "agent").addConditionalEdges("agent", route, { [END]: END, agent: "agent", deadLetter: "deadLetter" })
  .addEdge("deadLetter", END).compile();
async function main() {
  const r = await graph.invoke({ task: "Explain circuit breakers", result: "", error: "", retries: 0, status: "pending" });
  console.log("Status:", r.status, "| Result:", (r.result || r.error).substring(0, 80));
}
main().catch(console.error);
