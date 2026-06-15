namespace AgentPatterns.Context;
public record Tool(string Name, string Description);
public class ToolProvider {
    private readonly Dictionary<string, Func<string, string>> _tools = new() {
        ["calculate"] = args => { try { return new System.Data.DataTable().Compute(args, null)?.ToString() ?? "error"; } catch { return "error"; } },
        ["getWeather"] = city => city switch { "London" => "15°C cloudy", "Tokyo" => "22°C sunny", _ => "unavailable" },
    };
    public List<Tool> ListTools() => _tools.Keys.Select(k => new Tool(k, $"Tool: {k}")).ToList();
    public string CallTool(string name, string args) {
        if (!_tools.ContainsKey(name)) throw new KeyNotFoundException($"Tool '{name}' not found");
        return _tools[name](args);
    }
}
