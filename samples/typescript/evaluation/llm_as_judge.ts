import { ChatAnthropic } from "@langchain/anthropic";
import { StateGraph, END, START, Annotation } from "@langchain/langgraph";

const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });

const StateAnnotation = Annotation.Root({
  task: Annotation<string>(),
  output: Annotation<string>(),
  verdict: Annotation<string>(),
  retries: Annotation<number>(),
});

type State = typeof StateAnnotation.State;

async function produce(state: State): Promise<Partial<State>> {
  const res = await llm.invoke(`Complete this task concisely: ${state.task}`);
  return { output: res.content as string };
}

async function judge(state: State): Promise<Partial<State>> {
  const prompt = `Task: ${state.task}\nOutput: ${state.output}\n\nReply with exactly APPROVED or REJECTED and one sentence reason.`;
  const res = await llm.invoke(prompt);
  return { verdict: res.content as string };
}

function route(state: State): string {
  if (state.verdict.startsWith("APPROVED")) return "end";
  if (state.retries >= 2) return "dead_letter";
  return "retry";
}

async function retry(state: State): Promise<Partial<State>> {
  console.log(`Retry #${state.retries + 1}. Verdict: ${state.verdict}`);
  return { retries: state.retries + 1, output: "" };
}

async function deadLetter(state: State): Promise<Partial<State>> {
  console.log(`Dead letter after ${state.retries} retries. Last verdict: ${state.verdict}`);
  return {};
}

const graph = new StateGraph(StateAnnotation)
  .addNode("produce", produce)
  .addNode("judge", judge)
  .addNode("retry", retry)
  .addNode("dead_letter", deadLetter)
  .addEdge(START, "produce")
  .addEdge("produce", "judge")
  .addConditionalEdges("judge", route, {
    end: END,
    retry: "retry",
    dead_letter: END,
  })
  .addEdge("retry", "produce")
  .compile();

async function main() {
  const result = await graph.invoke({
    task: "Explain recursion in one sentence.",
    output: "",
    verdict: "",
    retries: 0,
  });
  console.log("Final output:", result.output);
  console.log("Final verdict:", result.verdict);
}

main().catch(console.error);
