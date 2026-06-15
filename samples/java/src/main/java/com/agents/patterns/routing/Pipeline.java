package com.agents.patterns.routing;

import org.springframework.ai.chat.client.ChatClient;

/**
 * Pattern: Pipeline
 * A task flows sequentially through a chain of agents where each agent's output
 * becomes the next agent's input. Planner → Executor → Verifier.
 */
public class Pipeline {

    /**
     * Runs a task through the planner → executor → verifier pipeline.
     * Each stage receives the previous stage's output as its input.
     *
     * @param planner  ChatClient that decomposes the task into steps
     * @param executor ChatClient that executes the plan
     * @param verifier ChatClient that verifies the execution result
     * @param task     the initial task description
     * @return the verifier's final verdict or refined output
     */
    public static String pipeline(ChatClient planner, ChatClient executor,
                                  ChatClient verifier, String task) {
        String plan = planner.prompt()
                .user("Create a step-by-step plan for: " + task)
                .call()
                .content();

        String execution = executor.prompt()
                .user("Execute this plan and return results:\n" + plan)
                .call()
                .content();

        return verifier.prompt()
                .user("Verify this execution result and provide a final summary:\n" + execution)
                .call()
                .content();
    }
}
