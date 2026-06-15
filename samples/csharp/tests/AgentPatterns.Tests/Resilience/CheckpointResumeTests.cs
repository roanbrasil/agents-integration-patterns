using AgentPatterns.Resilience;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Resilience;
public class CheckpointResumeTests {
    [Fact] public async Task RunWithCheckpoints_SavesAllSteps() {
        var mock = new Mock<IChatCompletionService>();
        mock.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "step result") });
        var steps = new List<string> { "gather", "analyze", "summarize" };
        var checkpoints = await CheckpointResume.RunWithCheckpoints(mock.Object, steps);
        checkpoints.Should().HaveCount(3);
        checkpoints.Should().AllSatisfy(c => c.Result.Should().Be("step result"));
    }
}
