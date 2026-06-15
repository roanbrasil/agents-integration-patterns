using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Coordination;
public class Orchestrator {
    public static async Task<string> Orchestrate(IChatCompletionService step1, IChatCompletionService step2, IChatCompletionService step3, string input) {
        var info = (await step1.GetChatMessageContentsAsync(new ChatHistory($"Gather facts about: {input}")))[0].Content ?? "";
        var analysis = (await step2.GetChatMessageContentsAsync(new ChatHistory($"Analyze: {info}")))[0].Content ?? "";
        return (await step3.GetChatMessageContentsAsync(new ChatHistory($"Summarize: {analysis}")))[0].Content ?? "";
    }
}
