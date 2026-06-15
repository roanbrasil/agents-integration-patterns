using AgentPatterns.Messaging;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Messaging;
public class BlackboardTests {
    [Fact] public void WriteAndRead_WorksCorrectly() {
        var board = new Blackboard();
        board.Write("problem", "optimize query performance");
        board.Read("problem").Should().Be("optimize query performance");
    }
    [Fact] public async Task AgentContribute_WritesToBoard() {
        var mock = new Mock<IChatCompletionService>();
        mock.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "use an index") });
        var board = new Blackboard();
        board.Write("problem", "slow queries");
        await board.AgentContribute(mock.Object, "solution", "problem");
        board.Read("solution").Should().Be("use an index");
    }
}
