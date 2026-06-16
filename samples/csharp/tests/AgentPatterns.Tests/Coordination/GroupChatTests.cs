using AgentPatterns.Coordination;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Coordination;
public class GroupChatTests {
    [Fact] public void ThreadStartsWithInput() {
        var chat = new GroupChat(GroupChat.MakerCheckerManager(), 4)
            .Add("maker", _ => "draft v1").Add("checker", _ => "APPROVED: good");
        chat.Run("write policy")[0].Should().Be(new Turn("input", "write policy"));
    }
    [Fact] public void StopsOnApproval() {
        var chat = new GroupChat(GroupChat.MakerCheckerManager(), 10)
            .Add("maker", _ => "draft v1").Add("checker", _ => "APPROVED: done");
        var thread = chat.Run("goal");
        thread[^1].Speaker.Should().Be("checker");
        thread[^1].Text.Should().Contain("APPROVED");
    }
    [Fact] public void IterationCapPreventsInfiniteLoop() {
        var chat = new GroupChat(GroupChat.MakerCheckerManager(), 4)
            .Add("maker", _ => "draft").Add("checker", _ => "REJECTED: nope");
        chat.Run("x").Should().HaveCount(5);
    }
    [Fact] public async Task RunWithLlm_CallsService() {
        var mock = new Mock<IChatCompletionService>();
        mock.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "APPROVED: done") });
        var thread = await GroupChat.RunWithLlm(mock.Object, "refund policy");
        thread.Should().NotBeEmpty();
    }
}
