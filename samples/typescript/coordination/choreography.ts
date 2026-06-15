interface AgentEvent { type: string; payload: string; }
const eventBus: AgentEvent[] = [];
function publish(e: AgentEvent) { eventBus.push(e); }
function subscribe(type: string): AgentEvent | undefined { return eventBus.find(e => e.type === type); }
async function agentA() {
  const ev = subscribe("task_created");
  if (!ev) return;
  const result = `[AgentA] processed: ${ev.payload}`;
  publish({ type: "data_ready", payload: result });
  return result;
}
async function agentB() {
  const ev = subscribe("data_ready");
  if (!ev) return;
  const result = `[AgentB] analyzed: ${ev.payload}`;
  publish({ type: "done", payload: result });
  return result;
}
async function main() {
  publish({ type: "task_created", payload: "analyze quarterly sales" });
  console.log("Events:", eventBus.map(e => e.type));
  await agentA();
  console.log("Events:", eventBus.map(e => e.type));
  await agentB();
  const done = subscribe("done");
  console.log("Final:", done?.payload);
}
main().catch(console.error);
