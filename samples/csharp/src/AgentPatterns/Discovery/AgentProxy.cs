using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Discovery;
public class AgentProxy {
    public static async Task<string> Proxy(IChatCompletionService backend, string task) {
        Console.WriteLine($"[Proxy] Forwarding task: {task.Substring(0, Math.Min(40, task.Length))}");
        var history = new ChatHistory($"Complete this task: {task}");
        var result = await backend.GetChatMessageContentsAsync(history);
        var response = result[0].Content ?? "";
        Console.WriteLine($"[Proxy] Got response ({response.Length} chars)");
        return response;
    }
}
