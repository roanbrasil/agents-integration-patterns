using AgentPatterns.Messaging;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Messaging;
public class DirectMessageTests {
    [Fact] public async Task Delegate_ReturnsAgentBResponse() {
        var mock = new Mock<IChatCompletionService>();
        mock.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "Task done by Agent B") });
        var result = await DirectMessage.Delegate(mock.Object, "Summarize the report");
        result.Should().Be("Task done by Agent B");
    }
}
