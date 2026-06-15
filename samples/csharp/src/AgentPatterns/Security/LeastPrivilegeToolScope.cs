namespace AgentPatterns.Security;
public class SecurityException(string message) : Exception(message);
public class LeastPrivilegeToolScope {
    private readonly HashSet<string> _allowed;
    public LeastPrivilegeToolScope(IEnumerable<string> tools) => _allowed = new HashSet<string>(tools);
    public string CallTool(string tool, string args) {
        if (!_allowed.Contains(tool)) throw new SecurityException($"Tool '{tool}' not in scope. Allowed: [{string.Join(", ", _allowed)}]");
        return $"[{tool}] executed: {args}";
    }
    public IReadOnlySet<string> AllowedTools => _allowed;
}
