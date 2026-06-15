from langchain_anthropic import ChatAnthropic
from typing import Any
import json

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

class ToolServer:
    """Simulated MCP Tool Server."""

    def list_tools(self) -> list[dict]:
        return [
            {
                "name": "calculate",
                "description": "Evaluate a math expression",
                "args": {"expression": "string — e.g. '2 + 3 * 4'"},
            },
            {
                "name": "get_weather",
                "description": "Get current weather for a city",
                "args": {"city": "string — e.g. 'Paris'"},
            },
        ]

    def call_tool(self, name: str, args: dict[str, Any]) -> str:
        if name == "calculate":
            try:
                result = eval(args["expression"], {"__builtins__": {}})
                return f"Result: {result}"
            except Exception as e:
                return f"Error: {e}"
        elif name == "get_weather":
            city = args.get("city", "Unknown")
            mock_weather = {
                "Paris": "Sunny, 22°C",
                "Tokyo": "Cloudy, 18°C",
                "New York": "Rainy, 15°C",
            }
            return mock_weather.get(city, f"Weather data unavailable for {city}")
        return f"Unknown tool: {name}"

def agent_reason_and_call(server: ToolServer, question: str) -> tuple:
    tools = server.list_tools()
    tools_description = json.dumps(tools, indent=2)

    plan_prompt = f"""You have access to these tools:
{tools_description}

Question: {question}

Reply with a JSON object only: {{"tool": "<name>", "args": {{...}}}}"""

    plan_response = llm.invoke(plan_prompt)
    raw = plan_response.content.strip()

    # Extract JSON from response
    start, end = raw.find("{"), raw.rfind("}") + 1
    tool_call = json.loads(raw[start:end])

    tool_result = server.call_tool(tool_call["tool"], tool_call["args"])

    answer_prompt = f"""Question: {question}
Tool used: {tool_call['tool']} with args {tool_call['args']}
Tool result: {tool_result}

Provide a concise final answer."""

    answer = llm.invoke(answer_prompt)
    return answer.content, tool_call, tool_result

def main():
    server = ToolServer()
    question = "What is the weather like in Tokyo right now?"

    print("=== Tool Provider Pattern ===")
    print(f"Question: {question}\n")

    print("Available tools:")
    for t in server.list_tools():
        print(f"  - {t['name']}: {t['description']}")

    answer, tool_call, tool_result = agent_reason_and_call(server, question)

    print(f"\nAgent chose tool: {tool_call['tool']} with args {tool_call['args']}")
    print(f"Tool result: {tool_result}")
    print(f"\nFinal Answer: {answer}")

if __name__ == "__main__":
    main()
