using AgentPatterns.Context;
using FluentAssertions;
namespace AgentPatterns.Tests.Context;
public class ToolProviderTests {
    [Fact] public void ListTools_ReturnsAvailableTools() {
        var provider = new ToolProvider();
        provider.ListTools().Should().HaveCountGreaterThan(0);
    }
    [Fact] public void CallTool_KnownTool_ReturnsResult() {
        var provider = new ToolProvider();
        provider.CallTool("getWeather", "Tokyo").Should().Be("22°C sunny");
    }
    [Fact] public void CallTool_UnknownTool_Throws() {
        var provider = new ToolProvider();
        provider.Invoking(p => p.CallTool("hack", "")).Should().Throw<KeyNotFoundException>();
    }
}
