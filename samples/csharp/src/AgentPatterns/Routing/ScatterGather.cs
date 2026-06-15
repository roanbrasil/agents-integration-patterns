using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Routing;
public class ScatterGather {
    public static async Task<string> Execute(IList<IChatCompletionService> agents, IChatCompletionService aggregator, string question) {
        var responses = await Task.WhenAll(agents.Select(async agent => {
            var h = new ChatHistory($"Answer briefly: {question}");
            return (await agent.GetChatMessageContentsAsync(h))[0].Content ?? "";
        }));
        var combined = string.Join("\n", responses.Select((r, i) => $"Agent {i+1}: {r}"));
        var aggHistory = new ChatHistory($"Synthesize these views on '{question}':\n{combined}");
        return (await aggregator.GetChatMessageContentsAsync(aggHistory))[0].Content ?? "";
    }
}
