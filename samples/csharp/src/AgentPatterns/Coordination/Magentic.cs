using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Coordination;
public class TaskLedger {
    public string Goal { get; }
    public List<string> Facts { get; } = new();
    public List<(string Step, string Result)> Done { get; } = new();
    public List<string> OpenQuestions { get; } = new();
    public TaskLedger(string goal) { Goal = goal; }
    public void Record(string step, string result) { Done.Add((step, result)); Facts.Add($"{step} -> {result}"); }
}
public class Magentic {
    private readonly Func<TaskLedger, List<string>> _planner;
    private readonly int _maxRounds;
    private readonly int _stallLimit;
    private readonly Dictionary<string, Func<string, string>> _specialists = new();
    public Magentic(Func<TaskLedger, List<string>> planner, int maxRounds = 8, int stallLimit = 2) {
        _planner = planner; _maxRounds = maxRounds; _stallLimit = stallLimit;
    }
    public Magentic Register(string name, Func<string, string> fn) { _specialists[name] = fn; return this; }
    public TaskLedger Run(string goal) {
        var ledger = new TaskLedger(goal);
        int stalls = 0;
        for (int round = 0; round < _maxRounds; round++) {
            var plan = _planner(ledger);
            if (!plan.Any()) return ledger;
            var nextStep = plan[0];
            var colon = nextStep.IndexOf(':');
            var name = colon > 0 ? nextStep[..colon].Trim() : nextStep;
            var task = colon > 0 ? nextStep[(colon + 1)..].Trim() : nextStep;
            if (_specialists.TryGetValue(name, out var specialist)) { ledger.Record(nextStep, specialist(task)); stalls = 0; }
            else { ledger.OpenQuestions.Add($"no specialist for: {nextStep}"); stalls++; }
            if (stalls >= _stallLimit) { ledger.OpenQuestions.Add("stalled — escalating"); return ledger; }
        }
        ledger.OpenQuestions.Add("round cap reached");
        return ledger;
    }
    public static async Task<TaskLedger> RunWithLlm(IChatCompletionService svc, string goal) {
        async Task<string> Invoke(string prompt) => (await svc.GetChatMessageContentsAsync(new ChatHistory(prompt)))[0].Content ?? "";
        var doneSteps = new HashSet<string>();
        Func<TaskLedger, List<string>> llmPlanner = ledger => {
            var response = Invoke($"Goal: {goal}. Completed: {string.Join(", ", ledger.Done.Select(d => d.Step))}. Specialists: researcher, writer. Return ONE step as 'specialist: task' or DONE.").GetAwaiter().GetResult();
            return response.Trim().ToUpper() == "DONE" || string.IsNullOrEmpty(response) ? new() : new() { response.Trim() };
        };
        return new Magentic(llmPlanner, 6, 2)
            .Register("researcher", task => Invoke($"Research (2 sentences): {task}").GetAwaiter().GetResult())
            .Register("writer", task => Invoke($"Write section (2 sentences): {task}").GetAwaiter().GetResult())
            .Run(goal);
    }
}
