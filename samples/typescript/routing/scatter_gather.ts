import { ChatAnthropic } from "@langchain/anthropic";
const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });
async function main() {
  const question = "What is the impact of AI on software engineering jobs?";
  const roles = ["optimist", "skeptic", "pragmatist"];
  const perspectives = await Promise.all(
    roles.map(role => llm.invoke(`You are a ${role}. In 2 sentences: ${question}`).then(r => ({ role, text: r.content as string })))
  );
  perspectives.forEach(p => console.log(`[${p.role}] ${p.text}\n`));
  const combined = perspectives.map(p => `${p.role}: ${p.text}`).join("\n");
  const synthesis = await llm.invoke(`Synthesize these views in 3 sentences:\n${combined}`);
  console.log("Synthesis:", synthesis.content as string);
}
main().catch(console.error);
