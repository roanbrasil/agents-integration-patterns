package com.agents.patterns.coordination;

import org.springframework.ai.chat.client.ChatClient;

import java.util.ArrayList;
import java.util.List;
import java.util.StringJoiner;

/**
 * Pattern: Supervised Delegation
 * A supervisor agent decomposes a goal into sub-tasks, delegates each sub-task
 * to a worker agent, then reviews all results before producing a final answer.
 */
public class SupervisedDelegation {

    /**
     * Supervisor splits the goal, workers execute sub-tasks, supervisor reviews.
     *
     * @param supervisor ChatClient that plans and reviews
     * @param workers    list of worker ChatClients
     * @param goal       the high-level goal to achieve
     * @return supervisor's final reviewed output
     */
    public static String supervise(ChatClient supervisor, List<ChatClient> workers, String goal) {
        String planPrompt = "Decompose the following goal into exactly "
                + workers.size() + " sub-tasks (one per line, no numbering):\n" + goal;
        String plan = supervisor.prompt().user(planPrompt).call().content();

        String[] subtasks = plan.split("\n");
        List<String> workerResults = new ArrayList<>();

        for (int i = 0; i < workers.size(); i++) {
            String subtask = (i < subtasks.length) ? subtasks[i].trim() : goal;
            String workerResult = workers.get(i).prompt()
                    .user("Complete this sub-task: " + subtask)
                    .call()
                    .content();
            workerResults.add("Worker " + (i + 1) + ": " + workerResult);
        }

        StringJoiner sj = new StringJoiner("\n");
        workerResults.forEach(sj::add);
        return supervisor.prompt()
                .user("Review worker results and provide the final answer:\n" + sj)
                .call()
                .content();
    }
}
