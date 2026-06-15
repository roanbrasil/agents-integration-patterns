package com.agents.patterns.messaging;

import org.springframework.ai.chat.client.ChatClient;

/**
 * Pattern: Direct Message
 * Agent A delegates a task directly to Agent B via ChatClient.
 * Models a point-to-point channel between two agents.
 */
public class DirectMessage {

    /**
     * Agent A asks Agent B to handle a task.
     *
     * @param chatClient the ChatClient representing Agent B
     * @param task       the task description to delegate
     * @return Agent B's response
     */
    public static String delegate(ChatClient chatClient, String task) {
        String prompt = "You are Agent B. Agent A has delegated the following task to you: " + task
                + "\nPlease complete the task and return your result.";

        return chatClient.prompt()
                .user(prompt)
                .call()
                .content();
    }
}
