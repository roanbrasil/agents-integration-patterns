using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Context;
public class ContextInjection {
    public static async Task<string> InjectAndQuery(IChatCompletionService svc, Dictionary<string, string> context, string question) {
        var ctx = string.Join("\n", context.Select(kv => $"{kv.Key}: {kv.Value}"));
        var history = new ChatHistory($"Use this context to answer:\n{ctx}\n\nQuestion: {question}");
        var result = await svc.GetChatMessageContentsAsync(history);
        return result[0].Content ?? "";
    }
}
