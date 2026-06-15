using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Security;
public enum TrustLevel { Untrusted, Gateway, Internal }
public class TrustBoundary {
    public static async Task<string> Forward(IChatCompletionService internalAgent, string request, TrustLevel level) {
        if (level == TrustLevel.Untrusted) throw new UnauthorizedAccessException("UNTRUSTED caller rejected at trust boundary");
        var h = new ChatHistory($"[{level}] Process: {request}");
        return (await internalAgent.GetChatMessageContentsAsync(h))[0].Content ?? "";
    }
}
