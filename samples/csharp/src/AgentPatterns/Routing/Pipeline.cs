using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Routing;
public class Pipeline {
    public static async Task<string> Execute(IChatCompletionService planner, IChatCompletionService executor, IChatCompletionService verifier, string task) {
        var plan = (await planner.GetChatMessageContentsAsync(new ChatHistory($"Plan: {task}")))[0].Content ?? "";
        var result = (await executor.GetChatMessageContentsAsync(new ChatHistory($"Execute: {plan}")))[0].Content ?? "";
        return (await verifier.GetChatMessageContentsAsync(new ChatHistory($"Verify result for task '{task}': {result}. Reply PASS or FAIL.")))[0].Content ?? "";
    }
}
