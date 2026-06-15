using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Evaluation;
public record EnsembleResult(string FinalVerdict, int Approvals, int Total);
public class EnsembleJudge {
    public static async Task<EnsembleResult> Evaluate(IList<IChatCompletionService> judges, string output, string task) {
        var verdicts = await Task.WhenAll(judges.Select(async judge => {
            var h = new ChatHistory($"Evaluate output for '{task}'. Output: {output}. Reply APPROVED or REJECTED.");
            var v = (await judge.GetChatMessageContentsAsync(h))[0].Content ?? "REJECTED";
            return v.ToUpper().Contains("APPROVED");
        }));
        var approvals = verdicts.Count(v => v);
        var verdict = approvals * 2 >= judges.Count ? "APPROVED" : "REJECTED";
        return new EnsembleResult(verdict, approvals, judges.Count);
    }
}
