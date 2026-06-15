from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

# Agent registry — simulates A2A service discovery
AGENT_REGISTRY: dict[str, dict] = {
    "agent_pdf_analyzer": {
        "id": "agent_pdf_analyzer",
        "capabilities": ["pdf_analysis", "document_extraction"],
        "endpoint": "local://agent_b",
    },
    "agent_web_scraper": {
        "id": "agent_web_scraper",
        "capabilities": ["web_scraping", "html_parsing"],
        "endpoint": "local://agent_c",
    },
}

def discover_agent(required_capability: str) -> dict | None:
    for agent_id, info in AGENT_REGISTRY.items():
        if required_capability in info["capabilities"]:
            print(f"[Registry] Found agent '{agent_id}' with capability '{required_capability}'")
            return info
    return None

# Agent B — the peer that handles PDF analysis
def agent_b_handle(task: str) -> str:
    print(f"[Agent B] Received delegation for: {task}")
    result = llm.invoke(
        f"You are a PDF analysis agent. Analyze this task and provide a 2-sentence result:\n{task}"
    )
    return result.content.strip()

# Simulate A2A call based on discovered endpoint
def delegate_to_peer(peer_info: dict, task: str) -> str:
    endpoint = peer_info["endpoint"]
    print(f"[A2A] Delegating to endpoint: {endpoint}")
    if endpoint == "local://agent_b":
        return agent_b_handle(task)
    return "Unknown peer endpoint."

# Agent A — discovers and delegates
def agent_a(task: str) -> str:
    print(f"[Agent A] Received task: {task}")
    required = "pdf_analysis"
    print(f"[Agent A] I lack capability '{required}', searching registry...")
    peer = discover_agent(required)
    if peer is None:
        return "[Agent A] No capable peer found. Cannot complete task."
    result = delegate_to_peer(peer, task)
    print(f"[Agent A] Got result from peer: {result}")
    return result

def main():
    task = "Extract the financial summary and key metrics from the Q1 2025 earnings PDF report."
    print("=== Peer-to-Peer Delegation (A2A) ===\n")
    final_result = agent_a(task)
    print(f"\n[Final Result]\n{final_result}")

if __name__ == "__main__":
    main()
