using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Resilience;
public class DeadLetterAgent {
    public static async Task<string> Process(IChatCompletionService agent, IChatCompletionService deadLetter, string task, int maxRetries = 2) {
        for (int attempt = 0; attempt <= maxRetries; attempt++) {
            try {
                var h = new ChatHistory($"Complete: {task}");
                return (await agent.GetChatMessageContentsAsync(h))[0].Content ?? "";
            } catch (Exception ex) when (attempt < maxRetries) {
                Console.WriteLine($"[DeadLetter] Attempt {attempt+1} failed: {ex.Message}. Retrying...");
            } catch (Exception ex) {
                Console.WriteLine($"[DeadLetter] All retries failed. Routing to dead letter: {ex.Message}");
                var dlH = new ChatHistory($"Handle failed task: {task}. Error: {ex.Message}");
                return "[DEAD LETTER] " + ((await deadLetter.GetChatMessageContentsAsync(dlH))[0].Content ?? "");
            }
        }
        return "";
    }
}
