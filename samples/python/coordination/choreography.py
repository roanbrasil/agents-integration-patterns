from typing import TypedDict
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

# Shared event bus — no central coordinator
event_bus: list[dict] = []

def publish(event_type: str, payload: str):
    event_bus.append({"type": event_type, "payload": payload})
    print(f"[Bus] Event published: {event_type}")

def consume(event_type: str) -> str | None:
    for event in event_bus:
        if event["type"] == event_type and not event.get("consumed"):
            event["consumed"] = True
            return event["payload"]
    return None

# Agent A: reacts to task_created, emits data_ready
def agent_a():
    payload = consume("task_created")
    if payload is None:
        print("[Agent A] No task_created event found.")
        return
    print(f"[Agent A] Processing task: {payload}")
    result = llm.invoke(f"Extract the key data points from this task in one sentence: {payload}")
    publish("data_ready", result.content.strip())
    print(f"[Agent A] Emitted data_ready: {result.content.strip()}")

# Agent B: reacts to data_ready, emits done
def agent_b():
    payload = consume("data_ready")
    if payload is None:
        print("[Agent B] No data_ready event found.")
        return
    print(f"[Agent B] Processing data: {payload}")
    result = llm.invoke(f"Write a brief completion report for this data in one sentence: {payload}")
    publish("done", result.content.strip())
    print(f"[Agent B] Emitted done: {result.content.strip()}")

def main():
    # Seed the initial event — no orchestrator decides what happens next
    publish("task_created", "Analyze sales trends in the European market for Q1 2025")

    # Each agent runs independently, reacting to events
    agent_a()
    agent_b()

    done_event = consume("done")
    if done_event:
        print(f"\n[Choreography Complete] Final result: {done_event}")
    print(f"\n[Event Bus History]")
    for e in event_bus:
        print(f"  {e['type']}: {e['payload'][:60]}...")

if __name__ == "__main__":
    main()
