package com.agents.patterns.resilience;

import org.springframework.ai.chat.client.ChatClient;

/**
 * Pattern: Dead-Letter Agent
 * When the primary agent fails repeatedly (up to maxRetries), the message is
 * forwarded to a dead-letter agent for safe handling (logging, quarantine, alert).
 */
public class DeadLetterAgent {

    /**
     * Attempts to process the task with the primary agent. On repeated failure,
     * falls back to the dead-letter agent.
     *
     * @param agent      the primary ChatClient agent
     * @param deadLetter the fallback dead-letter ChatClient agent
     * @param task       the task to process
     * @param maxRetries number of attempts before routing to dead-letter
     * @return the successful response (from primary or dead-letter)
     */
    public static String process(ChatClient agent, ChatClient deadLetter,
                                 String task, int maxRetries) {
        int attempts = 0;
        Exception lastException = null;

        while (attempts < maxRetries) {
            try {
                return agent.prompt()
                        .user(task)
                        .call()
                        .content();
            } catch (Exception e) {
                lastException = e;
                attempts++;
            }
        }

        String dlPrompt = "DEAD LETTER: The following task could not be processed after "
                + maxRetries + " retries. Task: " + task
                + "\nLast error: " + (lastException != null ? lastException.getMessage() : "unknown");

        return deadLetter.prompt()
                .user(dlPrompt)
                .call()
                .content();
    }
}
