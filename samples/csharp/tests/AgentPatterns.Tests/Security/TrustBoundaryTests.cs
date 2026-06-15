using AgentPatterns.Security;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Security;
public class TrustBoundaryTests {
    [Fact] public async Task Forward_UntrustedLevel_Throws() {
        var mock = new Mock<IChatCompletionService>();
        await FluentActions.Awaiting(() => TrustBoundary.Forward(mock.Object, "get secrets", TrustLevel.Untrusted))
            .Should().ThrowAsync<UnauthorizedAccessException>();
    }
    [Fact] public async Task Forward_GatewayLevel_Succeeds() {
        var mock = new Mock<IChatCompletionService>();
        mock.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "processed") });
        var result = await TrustBoundary.Forward(mock.Object, "get status", TrustLevel.Gateway);
        result.Should().Be("processed");
    }
}
