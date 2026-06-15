import { ChatAnthropic } from "@langchain/anthropic";

interface AgentCard {
  name: string;
  capabilities: string[];
  endpoint: string;
}

const registry: AgentCard[] = [
  {
    name: "SummaryAgent",
    capabilities: ["summarize", "condense"],
    endpoint: "agent://summary",
  },
  {
    name: "TranslationAgent",
    capabilities: ["translate", "localize"],
    endpoint: "agent://translation",
  },
  {
    name: "AnalysisAgent",
    capabilities: ["analyze", "classify", "extract"],
    endpoint: "agent://analysis",
  },
];

function findByCapability(cap: string): AgentCard | undefined {
  return registry.find((card) =>
    card.capabilities.some((c) => c.toLowerCase() === cap.toLowerCase())
  );
}

async function main() {
  const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });

  const requiredCapability = "summarize";
  const agent = findByCapability(requiredCapability);

  if (!agent) {
    console.log(`No agent found for capability: ${requiredCapability}`);
    return;
  }

  console.log(`Routing to agent: ${agent.name} at ${agent.endpoint}`);

  const task = "Summarize the key benefits of microservices architecture.";
  const res = await llm.invoke(
    `You are ${agent.name}. Your task: ${task}`
  );
  const text = res.content as string;

  console.log(`\nAgent response:\n${text}`);
}

main().catch(console.error);
