using AgentPatterns.Routing;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Routing;
public class ContentBasedRouterTests {
    [Fact] public async Task Route_ClassifiesAndDelegates() {
        var classifier = new Mock<IChatCompletionService>();
        classifier.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "coding") });
        var specialist = new Mock<IChatCompletionService>();
        specialist.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "Use recursion") });
        var result = await ContentBasedRouter.Route(classifier.Object, specialist.Object, "How to sort a list?");
        result.Should().Be("Use recursion");
    }
}
