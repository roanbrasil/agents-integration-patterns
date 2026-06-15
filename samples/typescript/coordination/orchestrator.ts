import { ChatAnthropic } from "@langchain/anthropic";
import { StateGraph, END, START, Annotation } from "@langchain/langgraph";
const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });
const State = Annotation.Root({
  topic: Annotation<string>(),
  info: Annotation<string>(),
  analysis: Annotation<string>(),
  summary: Annotation<string>(),
});
type S = typeof State.State;
const gather = async (s: S): Promise<Partial<S>> => ({ info: (await llm.invoke(`List 3 key facts about: ${s.topic}`)).content as string });
const analyze = async (s: S): Promise<Partial<S>> => ({ analysis: (await llm.invoke(`Analyze these facts:\n${s.info}`)).content as string });
const summarize = async (s: S): Promise<Partial<S>> => ({ summary: (await llm.invoke(`Summarize in 2 sentences:\n${s.analysis}`)).content as string });
const graph = new StateGraph(State)
  .addNode("gather", gather).addNode("analyze", analyze).addNode("summarize", summarize)
  .addEdge(START, "gather").addEdge("gather", "analyze").addEdge("analyze", "summarize").addEdge("summarize", END)
  .compile();
async function main() {
  const r = await graph.invoke({ topic: "Kubernetes", info: "", analysis: "", summary: "" });
  console.log("Summary:", r.summary);
}
main().catch(console.error);
