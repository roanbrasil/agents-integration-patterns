package com.agents.patterns.coordination;

import org.springframework.ai.chat.client.ChatClient;

/**
 * Pattern: Orchestrator
 * A central orchestrator coordinates a fixed sequence of agents, explicitly passing
 * the accumulated state from one step to the next. Unlike a pipeline, the orchestrator
 * maintains control and can inspect state between steps.
 */
public class Orchestrator {

    /**
     * Runs input through three sequential steps, threading state between them.
     *
     * @param step1 first agent ChatClient
     * @param step2 second agent ChatClient
     * @param step3 third agent ChatClient
     * @param input the initial input
     * @return output of the final step
     */
    public static String orchestrate(ChatClient step1, ChatClient step2,
                                     ChatClient step3, String input) {
        String state1 = step1.prompt()
                .user("[Step 1] Process this input: " + input)
                .call()
                .content();

        String state2 = step2.prompt()
                .user("[Step 2] Refine the following output from Step 1:\n" + state1)
                .call()
                .content();

        return step3.prompt()
                .user("[Step 3] Finalise based on Step 2 output:\n" + state2)
                .call()
                .content();
    }
}
