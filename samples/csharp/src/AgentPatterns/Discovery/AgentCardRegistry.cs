using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Discovery;
public record AgentCard(string Name, string Capability, string Endpoint);
public class AgentCardRegistry {
    private readonly List<AgentCard> _cards = new();
    public void Register(AgentCard card) => _cards.Add(card);
    public AgentCard? FindByCapability(string cap) => _cards.FirstOrDefault(c => c.Capability.Contains(cap, StringComparison.OrdinalIgnoreCase));
}
