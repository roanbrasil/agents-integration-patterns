using AgentPatterns.Resilience;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Resilience;
public class DeadLetterAgentTests {
    [Fact] public async Task Process_RoutesToDeadLetterOnMaxRetries() {
        var agent = new Mock<IChatCompletionService>();
        agent.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ThrowsAsync(new Exception("Service unavailable"));
        var deadLetter = new Mock<IChatCompletionService>();
        deadLetter.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "Logged failure") });
        var result = await DeadLetterAgent.Process(agent.Object, deadLetter.Object, "analyze data", maxRetries: 1);
        result.Should().StartWith("[DEAD LETTER]");
    }
    [Fact] public async Task Process_ReturnsResultOnSuccess() {
        var agent = new Mock<IChatCompletionService>();
        agent.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "success") });
        var dl = new Mock<IChatCompletionService>();
        var result = await DeadLetterAgent.Process(agent.Object, dl.Object, "task");
        result.Should().Be("success");
    }
}
