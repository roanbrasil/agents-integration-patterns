using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Coordination;
public class SupervisedDelegation {
    public static async Task<string> Supervise(IChatCompletionService supervisor, IList<IChatCompletionService> workers, string goal) {
        var workerResults = await Task.WhenAll(workers.Select(async (w, i) => {
            var h = new ChatHistory($"Worker {i+1}: contribute to goal: {goal}");
            return (await w.GetChatMessageContentsAsync(h))[0].Content ?? "";
        }));
        var combined = string.Join("\n", workerResults.Select((r, i) => $"Worker {i+1}: {r}"));
        var reviewHistory = new ChatHistory($"Supervisor: synthesize these results for goal '{goal}':\n{combined}");
        return (await supervisor.GetChatMessageContentsAsync(reviewHistory))[0].Content ?? "";
    }
}
