from langchain_anthropic import ChatAnthropic
from typing import TypedDict, List


class ScopedToolServer:
    def __init__(self, allowed_tools: List[str]):
        self.allowed_tools = allowed_tools

    def call(self, tool: str, arg: str) -> str:
        if tool not in self.allowed_tools:
            raise PermissionError(
                f"Tool '{tool}' is out of scope. Allowed: {self.allowed_tools}"
            )
        return f"[{tool}] executed with arg='{arg}'"


class ResearchAgent:
    def __init__(self, llm, server: ScopedToolServer):
        self.llm = llm
        self.server = server

    def run(self, query: str) -> str:
        plan = self.llm.invoke(
            f"You are a research agent. Given the query '{query}', "
            "reply with only: TOOL: search ARG: <short keyword>"
        )
        line = plan.content.strip()
        parts = line.split()
        tool = parts[1] if len(parts) > 1 else "search"
        arg = parts[3] if len(parts) > 3 else query
        return self.server.call(tool, arg)


class ExecutionAgent:
    def __init__(self, llm, server: ScopedToolServer):
        self.llm = llm
        self.server = server

    def run(self, task: str) -> str:
        plan = self.llm.invoke(
            f"You are an execution agent. Given the task '{task}', "
            "reply with only: TOOL: write ARG: <short description>"
        )
        line = plan.content.strip()
        parts = line.split()
        tool = parts[1] if len(parts) > 1 else "write"
        arg = parts[3] if len(parts) > 3 else task
        return self.server.call(tool, arg)


def main():
    llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

    research_server = ScopedToolServer(["search", "read"])
    execution_server = ScopedToolServer(["write", "run"])

    research_agent = ResearchAgent(llm, research_server)
    execution_agent = ExecutionAgent(llm, execution_server)

    print("=== Least-Privilege Tool Scope Demo ===\n")

    result = research_agent.run("latest AI papers")
    print(f"Research agent (search): {result}")

    try:
        research_server.call("write", "malicious output")
    except PermissionError as e:
        print(f"Research agent blocked from 'write': {e}")

    result = execution_agent.run("save report to disk")
    print(f"Execution agent (write): {result}")

    try:
        execution_server.call("search", "sensitive data")
    except PermissionError as e:
        print(f"Execution agent blocked from 'search': {e}")


if __name__ == "__main__":
    main()
