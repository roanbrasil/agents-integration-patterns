import { ChatAnthropic } from "@langchain/anthropic";
import { StateGraph, END, START, Annotation } from "@langchain/langgraph";

const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });

const StateAnnotation = Annotation.Root({
  question: Annotation<string>(),
  answer: Annotation<string>(),
});

type State = typeof StateAnnotation.State;

async function agentA(state: State): Promise<Partial<State>> {
  const res = await llm.invoke("Generate a short, interesting trivia question.");
  return { question: res.content as string };
}

async function agentB(state: State): Promise<Partial<State>> {
  const res = await llm.invoke(`Answer this question briefly: ${state.question}`);
  return { answer: res.content as string };
}

async function main() {
  const graph = new StateGraph(StateAnnotation)
    .addNode("agentA", agentA)
    .addNode("agentB", agentB)
    .addEdge(START, "agentA")
    .addEdge("agentA", "agentB")
    .addEdge("agentB", END)
    .compile();

  const result = await graph.invoke({ question: "", answer: "" });
  console.log("Question:", result.question);
  console.log("Answer:", result.answer);
}

main().catch(console.error);
