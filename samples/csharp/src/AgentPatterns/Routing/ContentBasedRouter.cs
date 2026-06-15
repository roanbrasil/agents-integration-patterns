using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Routing;
public class ContentBasedRouter {
    public static async Task<string> Route(IChatCompletionService classifier, IChatCompletionService specialist, string task) {
        var classifyHistory = new ChatHistory($"Classify into one word: coding, research, or data. Task: {task}. One word only.");
        var category = (await classifier.GetChatMessageContentsAsync(classifyHistory))[0].Content ?? "research";
        var specialistHistory = new ChatHistory($"You are a {category.Trim()} specialist. Answer: {task}");
        return (await specialist.GetChatMessageContentsAsync(specialistHistory))[0].Content ?? "";
    }
}
