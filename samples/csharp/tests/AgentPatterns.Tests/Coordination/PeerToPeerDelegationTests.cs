using AgentPatterns.Coordination;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Coordination;
public class PeerToPeerDelegationTests {
    [Fact] public async Task Delegate_FindsPeerAndDelegates() {
        var mock = new Mock<IChatCompletionService>();
        mock.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "translated text") });
        var pool = new Dictionary<string, IChatCompletionService> { ["translate"] = mock.Object };
        var result = await PeerToPeerDelegation.Delegate(pool, "translate", "Translate: hello world");
        result.Should().Be("translated text");
    }
    [Fact] public async Task Delegate_ThrowsWhenCapabilityNotFound() {
        var pool = new Dictionary<string, IChatCompletionService>();
        await FluentActions.Awaiting(() => PeerToPeerDelegation.Delegate(pool, "ocr", "task")).Should().ThrowAsync<KeyNotFoundException>();
    }
}
