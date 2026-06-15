using AgentPatterns.Context;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Context;
public class ContextInjectionTests {
    [Fact] public async Task InjectAndQuery_PassesContextToService() {
        var mock = new Mock<IChatCompletionService>();
        mock.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "Alice is an engineer") });
        var context = new Dictionary<string, string> { ["user"] = "Alice, engineer" };
        var result = await ContextInjection.InjectAndQuery(mock.Object, context, "Who is Alice?");
        result.Should().Be("Alice is an engineer");
    }
}
