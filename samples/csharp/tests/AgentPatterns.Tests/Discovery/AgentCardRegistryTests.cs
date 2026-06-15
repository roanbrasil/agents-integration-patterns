using AgentPatterns.Discovery;
using FluentAssertions;
namespace AgentPatterns.Tests.Discovery;
public class AgentCardRegistryTests {
    [Fact] public void FindByCapability_ReturnsMatchingAgent() {
        var registry = new AgentCardRegistry();
        registry.Register(new AgentCard("TranslationAgent", "translate-pdf", "http://agent1"));
        registry.Register(new AgentCard("SummaryAgent", "summarize", "http://agent2"));
        var found = registry.FindByCapability("translate");
        found.Should().NotBeNull();
        found!.Name.Should().Be("TranslationAgent");
    }
    [Fact] public void FindByCapability_ReturnsNullWhenNotFound() {
        var registry = new AgentCardRegistry();
        registry.FindByCapability("unknown").Should().BeNull();
    }
}
