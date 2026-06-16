import { ChatAnthropic } from "@langchain/anthropic";
const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });

interface TaskLedger {
  goal: string;
  facts: string[];
  plan: string[];
  done: [string, string][];
  openQuestions: string[];
}

type Specialist = (task: string) => Promise<string>;
type Planner = (ledger: TaskLedger) => Promise<string[]>;

class MagenticManager {
  private specialists: Map<string, Specialist> = new Map();
  constructor(private planner: Planner, private maxRounds = 8, private stallLimit = 2) {}
  register(name: string, fn: Specialist): this { this.specialists.set(name, fn); return this; }
  async run(goal: string): Promise<TaskLedger> {
    const ledger: TaskLedger = { goal, facts: [], plan: [], done: [], openQuestions: [] };
    let stalls = 0;
    for (let round = 0; round < this.maxRounds; round++) {
      ledger.plan = await this.planner(ledger);
      if (!ledger.plan.length) return ledger;
      const nextStep = ledger.plan[0];
      const [name, ...rest] = nextStep.split(":");
      const specialist = this.specialists.get(name.trim());
      if (specialist) {
        const result = await specialist(rest.join(":").trim() || nextStep);
        ledger.done.push([nextStep, result]);
        ledger.facts.push(`${nextStep} -> ${result}`);
        stalls = 0;
      } else {
        ledger.openQuestions.push(`no specialist for: ${nextStep}`);
        stalls++;
      }
      if (stalls >= this.stallLimit) { ledger.openQuestions.push("stalled — escalating"); return ledger; }
    }
    ledger.openQuestions.push("round cap reached");
    return ledger;
  }
}

async function main() {
  console.log("=== Magentic Orchestration ===\n");
  const planner: Planner = async (ledger) => {
    const doneSteps = new Set(ledger.done.map(([s]) => s));
    const r = await llm.invoke(`Planner for goal: "${ledger.goal}". Completed: ${[...doneSteps].join(", ") || "none"}. Available specialists: researcher, writer. Return ONE next step as "specialist: task" or "DONE".`);
    const text = (r.content as string).trim();
    return text.toUpperCase() === "DONE" || !text ? [] : [text];
  };
  const researcher: Specialist = async (task) => (await llm.invoke(`Research briefly (2 sentences): ${task}`)).content as string;
  const writer: Specialist = async (task) => (await llm.invoke(`Write a short section (2 sentences): ${task}`)).content as string;
  const mgr = new MagenticManager(planner, 6, 2).register("researcher", researcher).register("writer", writer);
  const ledger = await mgr.run("produce a competitive analysis of Python vs TypeScript for AI agents");
  console.log("Goal:", ledger.goal);
  console.log("Steps completed:", ledger.done.length);
  for (const [step, result] of ledger.done) console.log(`  [${step}] ${(result as string).substring(0, 80)}`);
  if (ledger.openQuestions.length) console.log("Open:", ledger.openQuestions);
}

main().catch(console.error);
