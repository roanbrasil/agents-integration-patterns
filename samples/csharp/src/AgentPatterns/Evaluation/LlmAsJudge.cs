using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Evaluation;
public record JudgeResult(string Output, string Verdict, int Retries);
public class LlmAsJudge {
    public static async Task<JudgeResult> Evaluate(IChatCompletionService producer, IChatCompletionService judge, string task, int maxRetries = 2) {
        for (int attempt = 0; attempt <= maxRetries; attempt++) {
            var prodH = new ChatHistory($"Complete this task: {task}");
            var output = (await producer.GetChatMessageContentsAsync(prodH))[0].Content ?? "";
            var judgeH = new ChatHistory($"Evaluate output for task '{task}'. Output: {output}. Reply APPROVED or REJECTED.");
            var verdict = (await judge.GetChatMessageContentsAsync(judgeH))[0].Content ?? "REJECTED";
            if (verdict.ToUpper().Contains("APPROVED")) return new JudgeResult(output, "APPROVED", attempt);
            if (attempt >= maxRetries) return new JudgeResult(output, "REJECTED", attempt);
        }
        return new JudgeResult("", "REJECTED", maxRetries);
    }
}
