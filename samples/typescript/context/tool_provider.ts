import { ChatAnthropic } from "@langchain/anthropic";
const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });
class ToolServer {
  listTools() {
    return [
      { name: "calculate", description: "Evaluate arithmetic expression", args: ["expr"] },
      { name: "getWeather", description: "Get mocked weather for city", args: ["city"] },
    ];
  }
  callTool(name: string, args: Record<string, string>): string {
    if (name === "calculate") return String(Function(`"use strict"; return (${args.expr})`)());
    if (name === "getWeather") return ({ London: "15°C cloudy", Tokyo: "22°C sunny", NYC: "10°C rainy" })[args.city] ?? "unavailable";
    return "unknown tool";
  }
}
async function main() {
  const server = new ToolServer();
  const toolList = server.listTools().map(t => `${t.name}: ${t.description}`).join("\n");
  const plan = await llm.invoke(`Tools:\n${toolList}\n\nWhich tool gets Tokyo weather? Reply: TOOL:<name> ARGS:<json>`);
  console.log("Plan:", plan.content as string);
  const result = server.callTool("getWeather", { city: "Tokyo" });
  const answer = await llm.invoke(`Tool returned: "${result}". Summarize for the user.`);
  console.log("Answer:", answer.content as string);
}
main().catch(console.error);
