using AgentPatterns.Coordination;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Coordination;
public class ChoreographyTests {
    [Fact] public async Task RunChoreography_ProducesEventChain() {
        var mock = new Mock<IChatCompletionService>();
        mock.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "processed") });
        var choreo = new Choreography();
        choreo.Publish(new AgentEvent("task_created", "analyze sales"));
        var events = await choreo.RunChoreography(mock.Object, mock.Object);
        events.Should().Contain(e => e.Type == "done");
    }
}
