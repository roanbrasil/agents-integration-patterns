using AgentPatterns.Resilience;
using FluentAssertions;
namespace AgentPatterns.Tests.Resilience;
public class CircuitBreakerTests {
    [Fact] public async Task CircuitOpensAfterThresholdFailures() {
        var cb = new CircuitBreaker(threshold: 2);
        for (int i = 0; i < 2; i++) {
            try { await cb.CallAsync(() => throw new Exception("fail")); } catch { }
        }
        cb.State.Should().Be(CircuitState.Open);
    }
    [Fact] public async Task OpenCircuitThrowsCircuitOpenException() {
        var cb = new CircuitBreaker(threshold: 1, timeoutMs: 60000);
        try { await cb.CallAsync(() => throw new Exception("fail")); } catch { }
        await FluentActions.Awaiting(() => cb.CallAsync(() => Task.FromResult("ok"))).Should().ThrowAsync<CircuitOpenException>();
    }
}
