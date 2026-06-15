using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Messaging;
public class DirectMessage {
    public static async Task<string> Delegate(IChatCompletionService svc, string task) {
        var history = new ChatHistory($"You are Agent B. Agent A delegated: {task}. Complete the task.");
        var result = await svc.GetChatMessageContentsAsync(history);
        return result[0].Content ?? "";
    }
}
