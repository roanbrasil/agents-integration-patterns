using AgentPatterns.Evaluation;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Evaluation;
public class EnsembleJudgeTests {
    [Fact] public async Task Evaluate_MajorityApproved_ReturnsApproved() {
        static Mock<IChatCompletionService> MakeMock(string verdict) {
            var m = new Mock<IChatCompletionService>();
            m.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
                .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, verdict) });
            return m;
        }
        var judges = new List<IChatCompletionService> { MakeMock("APPROVED").Object, MakeMock("APPROVED").Object, MakeMock("REJECTED").Object };
        var result = await EnsembleJudge.Evaluate(judges, "good answer", "summarize");
        result.FinalVerdict.Should().Be("APPROVED");
        result.Approvals.Should().Be(2);
        result.Total.Should().Be(3);
    }
}
