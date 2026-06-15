import { ChatAnthropic } from "@langchain/anthropic";

type AgentFn = (task: string) => Promise<string>;

function createProxy(agentFn: AgentFn, maxRetries = 2): AgentFn {
  return async (task: string): Promise<string> => {
    let attempt = 0;
    while (attempt <= maxRetries) {
      console.log(`[Proxy] Attempt ${attempt + 1} for task: "${task}"`);
      const start = Date.now();
      try {
        const result = await agentFn(task);
        const elapsed = Date.now() - start;
        console.log(`[Proxy] Success in ${elapsed}ms`);
        return result;
      } catch (err) {
        const elapsed = Date.now() - start;
        console.error(`[Proxy] Attempt ${attempt + 1} failed after ${elapsed}ms:`, err);
        attempt++;
        if (attempt > maxRetries) {
          throw new Error(`[Proxy] All ${maxRetries + 1} attempts failed.`);
        }
        console.log(`[Proxy] Retrying...`);
      }
    }
    throw new Error("[Proxy] Unexpected exit from retry loop.");
  };
}

async function coreAgent(task: string): Promise<string> {
  const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });
  const res = await llm.invoke(task);
  return res.content as string;
}

async function main() {
  const proxiedAgent = createProxy(coreAgent, 2);

  const task = "List three advantages of using an agent proxy pattern in distributed systems.";
  const result = await proxiedAgent(task);

  console.log(`\nResult:\n${result}`);
}

main().catch(console.error);
