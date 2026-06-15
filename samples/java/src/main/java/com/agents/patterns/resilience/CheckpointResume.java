package com.agents.patterns.resilience;

import org.springframework.ai.chat.client.ChatClient;

import java.util.ArrayList;
import java.util.List;

/**
 * Pattern: Checkpoint and Resume
 * Each step in a long-running agent workflow is checkpointed immediately after
 * completion. On failure, the workflow can resume from the last saved checkpoint
 * rather than restarting from scratch.
 */
public class CheckpointResume {

    public record Checkpoint(String stepName, String result) {}

    /**
     * Executes each step via the agent and records a checkpoint after each success.
     *
     * @param agent the ChatClient agent to execute each step
     * @param steps ordered list of step descriptions
     * @return list of completed checkpoints (one per step)
     */
    public static List<Checkpoint> runWithCheckpoints(ChatClient agent, List<String> steps) {
        List<Checkpoint> checkpoints = new ArrayList<>();

        for (String step : steps) {
            String result = agent.prompt()
                    .user("Execute this step: " + step)
                    .call()
                    .content();
            checkpoints.add(new Checkpoint(step, result));
        }

        return checkpoints;
    }
}
