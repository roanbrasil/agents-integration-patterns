# Trust Boundary

**Category:** Security
**Maturity:** ★ Emerging
**Also known as:** Trust Zone, Security Perimeter, Trust Tier

## Intent

Explicitly define which agents trust which other agents, and at what level, preventing unauthorized task delegation, impersonation, or data access across a multi-agent system.

## Context

You operate a multi-agent system where agents communicate over A2A (or any agent-to-agent channel), and at least some agents are reachable from outside a trusted core — exposed to external callers, untrusted content, or third-party agents.

## Problem

In an open agent network, a compromised or malicious actor can impersonate a trusted agent, inject malicious tasks through agent-to-agent channels, or escalate from a low-trust edge into the high-trust core. Without explicit trust levels, every agent implicitly trusts every caller — so one compromised agent compromises the whole mesh.

## Forces

- **F7 Trust asymmetry** — external callers and internal agents cannot be treated identically, but the more boundaries you enforce, the more authentication overhead every interaction carries.
- **F5 Blast radius** — tiering trust contains lateral movement on compromise, but...
- **F1 Latency / F11 Operational complexity** — every boundary crossing adds an auth check, key management, and a place for legitimate collaboration to be wrongly blocked.

Trust Boundary spends latency and operational complexity to buy containment (F5) under trust asymmetry (F7).

## Solution

Define trust tiers explicitly — typically **Untrusted** (external), **Gateway** (authenticated boundary), and **Internal** (core agents, full trust). Agents verify the identity of callers via Agent Card authentication (OAuth / bearer tokens) before accepting tasks. Capabilities available to a caller are a function of its tier: a Gateway-tier caller gets a sanitized, capability-restricted view; only Internal-tier callers reach sensitive operations.

This is defense in depth: the perimeter is not the only control — internal tiers limit how far a breach can spread.

![Trust Boundary](../../img/trust-boundary.svg)

## Sample Code

Runnable, tested implementation: [`samples/security/trust_boundary/`](../../samples/security/trust_boundary/)

```python
# Excerpt — tier determines what a caller may do
tier = classify_caller(token)          # UNTRUSTED | GATEWAY | INTERNAL
if tier is TrustTier.UNTRUSTED:
    raise Rejected("untrusted caller")
task = sanitize_for_tier(task, tier)   # Gateway gets a restricted view
return process(task, tier=tier)
```

## Consequences

- ✅ Defense in depth — perimeter plus internal trust levels (resolves F5, F7).
- ✅ Limits lateral movement: a breached edge agent cannot act as a core agent.
- ❌ Trust decisions must be maintained as the system evolves; stale tiers are a liability.
- ❌ Overly strict internal tiers slow legitimate agent collaboration (introduces F1, F11).

## Failure Modes Mitigated

Per [FAILURE-MAP.md](../FAILURE-MAP.md):

- **FM-2.3 Task derailment** ◐ — injected malicious tasks from untrusted callers are rejected at the boundary before they can derail the workflow.
- **FM-3.3 Incorrect verification** ◐ — prevents a compromised agent from impersonating a trusted verifier.

Beyond MAST, this pattern is the primary defense against **Agent-in-the-Middle (AiTM)** attacks and **A2A/MCP protocol confusion and downgrade** attacks, which arise specifically because the two protocols operate under different trust assumptions.

## Known Uses

- A2A authentication via Agent Cards (bearer/OAuth schemes in the Agent Card `authentication` block).
- Enterprise agent-mesh security architectures.
- Gateway/zone segmentation in production agent deployments.

## Related Patterns

- *uses* **[Agent Proxy](../discovery/agent-proxy.md)** — the gateway tier is often implemented as a proxy.
- *complements* **[Least-Privilege Tool Scope](least-privilege-tool-scope.md)** — Trust Boundary controls *who* can call; Least-Privilege controls *what* they can do once trusted.
- *complements* **[Prompt Firewall](prompt-firewall.md)** — boundary authenticates callers; firewall sanitizes the content they send.

## References

- *From Glue-Code to Protocols: A Critical Analysis of A2A and MCP Security.* arXiv:2505.03864.
- *A Survey of Agent Interoperability Protocols (MCP, ACP, A2A, ANP).* arXiv:2505.02279.
- Lee, D. & Tiwari, M. (2024). *Prompt Infection.* arXiv:2410.07283.
