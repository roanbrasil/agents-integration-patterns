using AgentPatterns.Routing;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Routing;
public class PipelineTests {
    [Fact] public async Task Execute_ChainsThreeSteps() {
        ChatMessageContent Make(string c) => new(AuthorRole.Assistant, c);
        var planner = new Mock<IChatCompletionService>();
        planner.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>())).ReturnsAsync(new List<ChatMessageContent> { Make("step-by-step plan") });
        var executor = new Mock<IChatCompletionService>();
        executor.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>())).ReturnsAsync(new List<ChatMessageContent> { Make("executed result") });
        var verifier = new Mock<IChatCompletionService>();
        verifier.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>())).ReturnsAsync(new List<ChatMessageContent> { Make("PASS") });
        var result = await Pipeline.Execute(planner.Object, executor.Object, verifier.Object, "sort a list");
        result.Should().Be("PASS");
    }
}
