package com.agents.patterns.coordination;
import org.springframework.ai.chat.client.ChatClient;
import java.util.*;
import java.util.function.Function;
public class Magentic {
    public record TaskLedger(String goal, List<String> facts, List<String[]> done, List<String> openQuestions) {
        public TaskLedger(String goal) { this(goal, new ArrayList<>(), new ArrayList<>(), new ArrayList<>()); }
        public void record(String step, String result) { done.add(new String[]{step, result}); facts.add(step + " -> " + result); }
    }
    @FunctionalInterface public interface Planner { List<String> plan(TaskLedger ledger); }
    private final Planner planner;
    private final int maxRounds;
    private final int stallLimit;
    private final Map<String, Function<String, String>> specialists = new LinkedHashMap<>();
    public Magentic(Planner planner, int maxRounds, int stallLimit) { this.planner = planner; this.maxRounds = maxRounds; this.stallLimit = stallLimit; }
    public Magentic register(String name, Function<String, String> specialist) { specialists.put(name, specialist); return this; }
    public TaskLedger run(String goal) {
        var ledger = new TaskLedger(goal);
        int stalls = 0;
        for (int round = 0; round < maxRounds; round++) {
            var plan = planner.plan(ledger);
            if (plan.isEmpty()) return ledger;
            String nextStep = plan.get(0);
            int colon = nextStep.indexOf(':');
            String name = colon > 0 ? nextStep.substring(0, colon).trim() : nextStep;
            String task = colon > 0 ? nextStep.substring(colon + 1).trim() : nextStep;
            var specialist = specialists.get(name);
            if (specialist != null) { ledger.record(nextStep, specialist.apply(task)); stalls = 0; }
            else { ledger.openQuestions().add("no specialist for: " + nextStep); stalls++; }
            if (stalls >= stallLimit) { ledger.openQuestions().add("stalled — escalating"); return ledger; }
        }
        ledger.openQuestions().add("round cap reached");
        return ledger;
    }
    public static TaskLedger runWithLlm(ChatClient chatClient, String goal) {
        Planner llmPlanner = ledger -> {
            Set<String> done = new HashSet<>();
            for (var s : ledger.done()) done.add(s[0]);
            String response = chatClient.prompt().user("Goal: " + goal + ". Completed: " + done + ". Specialists: researcher, writer. Return ONE step as 'specialist: task' or DONE.").call().content();
            if (response == null || response.trim().toUpperCase().equals("DONE")) return List.of();
            return List.of(response.trim());
        };
        return new Magentic(llmPlanner, 6, 2)
            .register("researcher", task -> chatClient.prompt().user("Research (2 sentences): " + task).call().content())
            .register("writer", task -> chatClient.prompt().user("Write section (2 sentences): " + task).call().content())
            .run(goal);
    }
}
