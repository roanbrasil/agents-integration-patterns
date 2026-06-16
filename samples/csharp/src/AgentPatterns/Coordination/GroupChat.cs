using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Coordination;
public record Turn(string Speaker, string Text);
public class GroupChat {
    public delegate string? Manager(IList<Turn> thread, IList<string> names);
    private readonly Manager _manager;
    private readonly int _maxTurns;
    private readonly Dictionary<string, Func<IList<Turn>, string>> _participants = new();
    public GroupChat(Manager manager, int maxTurns = 10) { _manager = manager; _maxTurns = maxTurns; }
    public GroupChat Add(string name, Func<IList<Turn>, string> agent) { _participants[name] = agent; return this; }
    public IList<Turn> Run(string opening) {
        var thread = new List<Turn> { new("input", opening) };
        var names = _participants.Keys.ToList();
        for (int i = 0; i < _maxTurns; i++) {
            var speaker = _manager(thread, names);
            if (speaker is null) return thread;
            thread.Add(new Turn(speaker, _participants[speaker](thread)));
        }
        return thread;
    }
    public static Manager MakerCheckerManager(string approveToken = "APPROVED") => (thread, _) => {
        for (int i = thread.Count - 1; i >= 0; i--) {
            if (thread[i].Speaker == "checker") {
                if (thread[i].Text.Contains(approveToken)) return null;
                break;
            }
        }
        return thread[^1].Speaker == "maker" ? "checker" : "maker";
    };
    public static async Task<IList<Turn>> RunWithLlm(IChatCompletionService svc, string goal) {
        async Task<string> Invoke(string prompt) {
            var h = new ChatHistory(prompt);
            return (await svc.GetChatMessageContentsAsync(h))[0].Content ?? "";
        }
        int drafts = 0;
        Func<IList<Turn>, string> maker = thread => {
            drafts++;
            var feedback = thread.LastOrDefault(t => t.Speaker == "checker")?.Text ?? "none yet";
            return Invoke($"Draft #{drafts}. Feedback: {feedback}. Write a 2-sentence draft for: {goal}").GetAwaiter().GetResult();
        };
        Func<IList<Turn>, string> checker = thread => {
            var draft = thread.LastOrDefault(t => t.Speaker == "maker")?.Text ?? "";
            return Invoke($"Review: {draft}. If good, start with APPROVED. Otherwise REJECTED with one line.").GetAwaiter().GetResult();
        };
        return new GroupChat(MakerCheckerManager(), 8).Add("maker", maker).Add("checker", checker).Run(goal);
    }
}
