using AgentPatterns.Evaluation;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Evaluation;
public class LlmAsJudgeTests {
    [Fact] public async Task Evaluate_ApprovedOnFirstAttempt() {
        var producer = new Mock<IChatCompletionService>();
        producer.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "good output") });
        var judge = new Mock<IChatCompletionService>();
        judge.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "APPROVED") });
        var result = await LlmAsJudge.Evaluate(producer.Object, judge.Object, "write summary");
        result.Verdict.Should().Be("APPROVED");
        result.Retries.Should().Be(0);
    }
    [Fact] public async Task Evaluate_ReturnsRejectedAfterMaxRetries() {
        var producer = new Mock<IChatCompletionService>();
        producer.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "poor output") });
        var judge = new Mock<IChatCompletionService>();
        judge.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "REJECTED") });
        var result = await LlmAsJudge.Evaluate(producer.Object, judge.Object, "write summary", maxRetries: 1);
        result.Verdict.Should().Be("REJECTED");
    }
}
