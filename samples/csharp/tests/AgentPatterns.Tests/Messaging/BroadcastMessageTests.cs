using AgentPatterns.Messaging;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Messaging;
public class BroadcastMessageTests {
    [Fact] public async Task Broadcast_ReturnsResponsesForAllRoles() {
        var mock = new Mock<IChatCompletionService>();
        mock.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "My reaction") });
        var roles = new List<string> { "optimist", "skeptic", "analyst" };
        var results = await BroadcastMessage.Broadcast(mock.Object, "AI will replace jobs", roles);
        results.Should().HaveCount(3);
        results.Should().AllSatisfy(r => r.Should().Be("My reaction"));
    }
}
