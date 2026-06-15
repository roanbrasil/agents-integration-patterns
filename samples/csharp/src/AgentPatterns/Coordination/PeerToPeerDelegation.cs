using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Coordination;
public class PeerToPeerDelegation {
    public static async Task<string> Delegate(Dictionary<string, IChatCompletionService> agentPool, string requiredCapability, string task) {
        if (!agentPool.TryGetValue(requiredCapability, out var peer))
            throw new KeyNotFoundException($"No agent found for capability: {requiredCapability}");
        var history = new ChatHistory($"You are a {requiredCapability} specialist. {task}");
        return (await peer.GetChatMessageContentsAsync(history))[0].Content ?? "";
    }
}
