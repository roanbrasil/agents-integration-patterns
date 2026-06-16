import { ChatAnthropic } from "@langchain/anthropic";
const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });

type Participant = (thread: [string, string][]) => Promise<string>;
type Manager = (thread: [string, string][], names: string[]) => string | null;

class GroupChat {
  private thread: [string, string][] = [];
  private participants: Map<string, Participant> = new Map();
  constructor(private manager: Manager, private maxTurns = 10) {}
  add(name: string, agent: Participant): this { this.participants.set(name, agent); return this; }
  async run(opening: string): Promise<[string, string][]> {
    this.thread = [["input", opening]];
    const names = [...this.participants.keys()];
    for (let i = 0; i < this.maxTurns; i++) {
      const speaker = this.manager(this.thread, names);
      if (!speaker) return this.thread;
      const agent = this.participants.get(speaker)!;
      const msg = await agent(this.thread);
      this.thread.push([speaker, msg]);
    }
    return this.thread;
  }
}

function makerCheckerManager(approveToken = "APPROVED"): Manager {
  return (thread, _names) => {
    for (let i = thread.length - 1; i >= 0; i--) {
      const [speaker, text] = thread[i];
      if (speaker === "checker") {
        if (text.includes(approveToken)) return null;
        break;
      }
    }
    const last = thread[thread.length - 1][0];
    return last === "maker" ? "checker" : "maker";
  };
}

async function main() {
  console.log("=== Group Chat — Maker-Checker ===\n");
  const maker: Participant = async (thread) => {
    const priorDrafts = thread.filter(([s]) => s === "maker").length;
    const feedback = [...thread].reverse().find(([s]) => s === "checker")?.[1] ?? "none yet";
    const r = await llm.invoke(`You are a writer. Draft #${priorDrafts + 1}. Feedback: ${feedback}. Write a 2-sentence refund policy draft.`);
    return r.content as string;
  };
  const checker: Participant = async (thread) => {
    const draft = [...thread].reverse().find(([s]) => s === "maker")?.[1] ?? "";
    const r = await llm.invoke(`You are a strict reviewer. Goal: clear refund policy. Draft: ${draft}. If good, start with APPROVED. Otherwise start with REJECTED and give one line of feedback.`);
    return r.content as string;
  };
  const chat = new GroupChat(makerCheckerManager(), 8).add("maker", maker).add("checker", checker);
  const thread = await chat.run("draft a refund policy for a SaaS product");
  for (const [speaker, text] of thread) {
    console.log(`[${speaker.padEnd(8)}] ${(text as string).substring(0, 100)}`);
  }
}

main().catch(console.error);
