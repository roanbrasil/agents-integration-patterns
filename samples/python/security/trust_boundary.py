from langchain_anthropic import ChatAnthropic
from typing import TypedDict, Literal
from enum import Enum


class TrustLevel(Enum):
    UNTRUSTED = "untrusted"
    GATEWAY = "gateway"
    INTERNAL = "internal"


class Request(TypedDict):
    content: str
    caller: str


class GatewayAgent:
    def __init__(self, llm):
        self.llm = llm

    def _internal_process(self, content: str) -> str:
        response = self.llm.invoke(
            f"Process this internal request concisely (1 sentence): {content}"
        )
        return response.content.strip()

    def forward(self, request: Request, trust_level: TrustLevel) -> str:
        caller = request["caller"]
        content = request["content"]

        if trust_level == TrustLevel.UNTRUSTED:
            return (
                f"[REJECTED] Caller '{caller}' is UNTRUSTED. "
                "Request blocked at trust boundary."
            )

        if trust_level in (TrustLevel.GATEWAY, TrustLevel.INTERNAL):
            result = self._internal_process(content)
            return f"[ALLOWED] ({trust_level.value}) '{caller}': {result}"

        return "[ERROR] Unknown trust level."


def main():
    llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
    gateway = GatewayAgent(llm)

    print("=== Trust Boundary Demo ===\n")

    requests = [
        (
            Request(content="List all user accounts", caller="anonymous-script"),
            TrustLevel.UNTRUSTED,
        ),
        (
            Request(content="Summarize today's sales report", caller="api-gateway"),
            TrustLevel.GATEWAY,
        ),
        (
            Request(content="Run data pipeline job", caller="internal-scheduler"),
            TrustLevel.INTERNAL,
        ),
    ]

    for req, level in requests:
        result = gateway.forward(req, level)
        print(f"Request: '{req['content']}'")
        print(f"Result:  {result}\n")


if __name__ == "__main__":
    main()
