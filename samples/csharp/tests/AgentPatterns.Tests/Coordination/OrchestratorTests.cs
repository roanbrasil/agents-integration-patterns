using AgentPatterns.Coordination;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Coordination;
public class OrchestratorTests {
    [Fact] public async Task Orchestrate_RunsThreeStepsSequentially() {
        static Mock<IChatCompletionService> MakeMock(string resp) {
            var m = new Mock<IChatCompletionService>();
            m.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
                .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, resp) });
            return m;
        }
        var result = await Orchestrator.Orchestrate(MakeMock("facts").Object, MakeMock("analysis").Object, MakeMock("summary").Object, "Kubernetes");
        result.Should().Be("summary");
    }
}
