package com.agents.patterns.coordination;
import org.springframework.ai.chat.client.ChatClient;
import java.util.*;
public class GroupChat {
    public record Turn(String speaker, String text) {}
    @FunctionalInterface public interface Manager { String next(List<Turn> thread, List<String> names); }
    private final Manager manager;
    private final int maxTurns;
    private final Map<String, java.util.function.Function<List<Turn>, String>> participants = new LinkedHashMap<>();
    public GroupChat(Manager manager, int maxTurns) { this.manager = manager; this.maxTurns = maxTurns; }
    public GroupChat add(String name, java.util.function.Function<List<Turn>, String> agent) { participants.put(name, agent); return this; }
    public List<Turn> run(String opening) {
        List<Turn> thread = new ArrayList<>();
        thread.add(new Turn("input", opening));
        List<String> names = new ArrayList<>(participants.keySet());
        for (int i = 0; i < maxTurns; i++) {
            String speaker = manager.next(thread, names);
            if (speaker == null) return thread;
            String msg = participants.get(speaker).apply(thread);
            thread.add(new Turn(speaker, msg));
        }
        return thread;
    }
    public static Manager makerCheckerManager(String approveToken) {
        return (thread, names) -> {
            for (int i = thread.size() - 1; i >= 0; i--) {
                Turn t = thread.get(i);
                if (t.speaker().equals("checker")) {
                    if (t.text().contains(approveToken)) return null;
                    break;
                }
            }
            String last = thread.get(thread.size() - 1).speaker();
            return last.equals("maker") ? "checker" : "maker";
        };
    }
    public static String runWithLlm(ChatClient chatClient, String goal) {
        java.util.function.Function<List<Turn>, String> maker = thread -> {
            long drafts = thread.stream().filter(t -> t.speaker().equals("maker")).count();
            String feedback = thread.stream().filter(t -> t.speaker().equals("checker")).reduce((a, b) -> b).map(Turn::text).orElse("none yet");
            return chatClient.prompt().user("Draft #" + (drafts + 1) + ". Feedback: " + feedback + ". Write a 2-sentence draft for: " + goal).call().content();
        };
        java.util.function.Function<List<Turn>, String> checker = thread -> {
            String draft = thread.stream().filter(t -> t.speaker().equals("maker")).reduce((a, b) -> b).map(Turn::text).orElse("");
            return chatClient.prompt().user("Review draft: " + draft + ". If acceptable, start with APPROVED. Otherwise REJECTED with one line feedback.").call().content();
        };
        GroupChat chat = new GroupChat(makerCheckerManager("APPROVED"), 8).add("maker", maker).add("checker", checker);
        return chat.run(goal).stream().map(t -> "[" + t.speaker() + "] " + t.text()).reduce("", (a, b) -> a + "\n" + b);
    }
}
