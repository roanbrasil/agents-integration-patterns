namespace AgentPatterns.Resilience;
public enum CircuitState { Closed, Open, HalfOpen }
public class CircuitOpenException(string message) : Exception(message);
public class CircuitBreaker {
    public CircuitState State { get; private set; } = CircuitState.Closed;
    private int _failures;
    private DateTime _openedAt;
    private readonly int _threshold;
    private readonly TimeSpan _timeout;
    public CircuitBreaker(int threshold = 3, int timeoutMs = 5000) { _threshold = threshold; _timeout = TimeSpan.FromMilliseconds(timeoutMs); }
    public async Task<string> CallAsync(Func<Task<string>> operation) {
        if (State == CircuitState.Open) {
            if (DateTime.UtcNow - _openedAt >= _timeout) State = CircuitState.HalfOpen;
            else throw new CircuitOpenException("Circuit is OPEN — call blocked");
        }
        try {
            var result = await operation();
            _failures = 0; State = CircuitState.Closed;
            return result;
        } catch (CircuitOpenException) { throw; }
        catch {
            _failures++;
            if (_failures >= _threshold) { State = CircuitState.Open; _openedAt = DateTime.UtcNow; }
            throw;
        }
    }
}
