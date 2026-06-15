using AgentPatterns.Routing;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Routing;
public class ScatterGatherTests {
    [Fact] public async Task Execute_CallsAllAgentsAndAggregates() {
        var agentMock = new Mock<IChatCompletionService>();
        agentMock.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "perspective") });
        var aggMock = new Mock<IChatCompletionService>();
        aggMock.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "synthesis") });
        var agents = new List<IChatCompletionService> { agentMock.Object, agentMock.Object, agentMock.Object };
        var result = await ScatterGather.Execute(agents, aggMock.Object, "Impact of AI?");
        result.Should().Be("synthesis");
    }
}
