using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Messaging;
public class BroadcastMessage {
    public static async Task<List<string>> Broadcast(IChatCompletionService svc, string message, List<string> roles) {
        var tasks = roles.Select(async role => {
            var history = new ChatHistory($"You are a {role}. React to this news: {message}");
            var r = await svc.GetChatMessageContentsAsync(history);
            return r[0].Content ?? "";
        });
        return (await Task.WhenAll(tasks)).ToList();
    }
}
