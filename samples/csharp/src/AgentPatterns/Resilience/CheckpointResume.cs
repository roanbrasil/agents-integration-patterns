using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Resilience;
public record Checkpoint(string StepName, string Result);
public class CheckpointResume {
    public static async Task<List<Checkpoint>> RunWithCheckpoints(IChatCompletionService svc, List<string> steps) {
        var checkpoints = new List<Checkpoint>();
        foreach (var step in steps) {
            var h = new ChatHistory($"Execute step: {step}");
            var result = (await svc.GetChatMessageContentsAsync(h))[0].Content ?? "";
            checkpoints.Add(new Checkpoint(step, result));
            Console.WriteLine($"[Checkpoint] '{step}' saved");
        }
        return checkpoints;
    }
}
