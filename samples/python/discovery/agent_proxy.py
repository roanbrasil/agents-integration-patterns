import time
from langchain_anthropic import ChatAnthropic
from typing import Callable

# --- Agent Proxy Pattern ---

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")


def underlying_agent(task: str) -> str:
    return llm.invoke(f"Complete this task concisely: {task}").content


def agent_proxy(
    task: str,
    agent_fn: Callable[[str], str],
    max_retries: int = 2,
) -> str:
    print(f"[Proxy] Received task: {task}")
    print(f"[Proxy] Translating protocol: raw string -> agent call")

    attempt = 0
    last_error = None

    while attempt <= max_retries:
        try:
            start = time.time()
            print(f"[Proxy] Attempt {attempt + 1}: calling underlying agent...")
            result = agent_fn(task)
            elapsed = time.time() - start
            print(f"[Proxy] Agent responded in {elapsed:.2f}s")
            print(f"[Proxy] Logging result (first 80 chars): {result[:80]!r}")
            return result
        except Exception as e:
            last_error = e
            attempt += 1
            print(f"[Proxy] Error on attempt {attempt}: {e}. Retrying...")

    raise RuntimeError(
        f"[Proxy] All {max_retries + 1} attempts failed. Last error: {last_error}"
    )


def main():
    task = "List 3 benefits of using an agent proxy pattern in distributed systems."
    print("=" * 60)
    print("Agent Proxy Pattern Demo")
    print("=" * 60)

    result = agent_proxy(task, underlying_agent)

    print("\n[Final Result]")
    print(result)


if __name__ == "__main__":
    main()
