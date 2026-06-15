using AgentPatterns.Security;
using FluentAssertions;
namespace AgentPatterns.Tests.Security;
public class LeastPrivilegeToolScopeTests {
    [Fact] public void CallTool_AllowedTool_ReturnsResult() {
        var scope = new LeastPrivilegeToolScope(new[] { "search", "read" });
        scope.CallTool("search", "AI papers").Should().Contain("search");
    }
    [Fact] public void CallTool_BlockedTool_ThrowsSecurityException() {
        var scope = new LeastPrivilegeToolScope(new[] { "search" });
        scope.Invoking(s => s.CallTool("write", "data")).Should().Throw<SecurityException>();
    }
}
