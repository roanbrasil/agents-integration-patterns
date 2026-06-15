import { ChatAnthropic } from "@langchain/anthropic";

const llm = new ChatAnthropic({ model: "claude-haiku-4-5-20251001" });

async function publisher(): Promise<string> {
  const res = await llm.invoke("Generate a one-sentence news headline about technology.");
  return res.content as string;
}

async function subscriber(role: string, topic: string): Promise<string> {
  const res = await llm.invoke(
    `You are a ${role}. React briefly to this headline: "${topic}"`
  );
  return res.content as string;
}

async function main() {
  const topic = await publisher();
  console.log("Publisher broadcast:", topic);

  const roles = ["skeptical journalist", "excited investor", "concerned ethicist"];
  const reactions = await Promise.all(
    roles.map((role) => subscriber(role, topic))
  );

  reactions.forEach((reaction, i) => {
    console.log(`\n[${roles[i]}]:`, reaction);
  });
}

main().catch(console.error);
