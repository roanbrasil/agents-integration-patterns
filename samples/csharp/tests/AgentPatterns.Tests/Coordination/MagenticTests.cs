using AgentPatterns.Coordination;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Moq;
using FluentAssertions;
namespace AgentPatterns.Tests.Coordination;
public class MagenticTests {
    [Fact] public void CleanCompletion() {
        var done = new HashSet<string>();
        var mgr = new Magentic(ledger => {
            if (!done.Contains("researcher: market")) return new() { "researcher: market" };
            if (!done.Contains("writer: analysis")) return new() { "writer: analysis" };
            return new();
        }, 8, 2)
        .Register("researcher", t => { done.Add("researcher: market"); return "found info"; })
        .Register("writer", t => { done.Add("writer: analysis"); return "wrote section"; });
        var ledger = mgr.Run("analysis");
        ledger.Done.Should().HaveCount(2);
        ledger.OpenQuestions.Should().BeEmpty();
    }
    [Fact] public void StallDetection() {
        var mgr = new Magentic(_ => new() { "ghost: step" }, 10, 2);
        var ledger = mgr.Run("impossible");
        ledger.OpenQuestions.Should().Contain(q => q.Contains("stalled"));
        ledger.Done.Should().BeEmpty();
    }
    [Fact] public void RoundCap() {
        int calls = 0;
        var mgr = new Magentic(_ => new() { "worker: step" }, 3, 99).Register("worker", _ => { calls++; return "ok"; });
        var ledger = mgr.Run("endless");
        calls.Should().Be(3);
        ledger.OpenQuestions.Should().Contain(q => q.Contains("round cap"));
    }
    [Fact] public async Task RunWithLlm_CallsService() {
        var mock = new Mock<IChatCompletionService>();
        mock.Setup(s => s.GetChatMessageContentsAsync(It.IsAny<ChatHistory>(), It.IsAny<PromptExecutionSettings>(), It.IsAny<Kernel>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<ChatMessageContent> { new(AuthorRole.Assistant, "DONE") });
        var ledger = await Magentic.RunWithLlm(mock.Object, "test goal");
        ledger.Should().NotBeNull();
    }
}
