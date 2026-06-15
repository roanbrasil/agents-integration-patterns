using Microsoft.SemanticKernel.ChatCompletion;
namespace AgentPatterns.Coordination;
public record AgentEvent(string Type, string Payload);
public class Choreography {
    public List<AgentEvent> EventBus { get; } = new();
    public void Publish(AgentEvent e) => EventBus.Add(e);
    public AgentEvent? Subscribe(string type) => EventBus.Find(e => e.Type == type);
    public async Task<List<AgentEvent>> RunChoreography(IChatCompletionService agentA, IChatCompletionService agentB) {
        var trigger = Subscribe("task_created");
        if (trigger != null) {
            var h = new ChatHistory($"Process: {trigger.Payload}");
            var rA = (await agentA.GetChatMessageContentsAsync(h))[0].Content ?? "";
            Publish(new AgentEvent("data_ready", rA));
            var dataEv = Subscribe("data_ready");
            if (dataEv != null) {
                var h2 = new ChatHistory($"Analyze: {dataEv.Payload}");
                var rB = (await agentB.GetChatMessageContentsAsync(h2))[0].Content ?? "";
                Publish(new AgentEvent("done", rB));
            }
        }
        return EventBus;
    }
}
