using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Messaging;
public class Blackboard {
    private readonly Dictionary<string, string> _board = new();
    public void Write(string key, string value) => _board[key] = value;
    public string Read(string key) => _board.TryGetValue(key, out var v) ? v : "";
    public async Task<string> AgentContribute(IChatCompletionService svc, string writeKey, string contextKey) {
        var ctx = Read(contextKey);
        var history = new ChatHistory($"Based on: {ctx}\nContribute your part. Be concise.");
        var r = await svc.GetChatMessageContentsAsync(history);
        var contribution = r[0].Content ?? "";
        Write(writeKey, contribution);
        return contribution;
    }
}
