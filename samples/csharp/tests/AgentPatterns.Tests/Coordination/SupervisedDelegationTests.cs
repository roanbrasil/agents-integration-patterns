using AgentPatterns.Coordination;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Coordination;
public class SupervisedDelegationTests {
    [Fact] public async Task Supervise_CombinesWorkerResults() {
        var workerMock = new Mock<IChatCompletionService>();
        workerMock.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "worker output") });
        var supervisorMock = new Mock<IChatCompletionService>();
        supervisorMock.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "final synthesis") });
        var result = await SupervisedDelegation.Supervise(supervisorMock.Object, new[] { workerMock.Object, workerMock.Object }, "analyze data");
        result.Should().Be("final synthesis");
    }
}
