package com.agents.patterns.routing;

import org.springframework.ai.chat.client.ChatClient;

/**
 * Pattern: Content-Based Router
 * A classifier agent inspects the incoming task and decides which specialist
 * agent should handle it. The task is then forwarded to the chosen specialist.
 */
public class ContentBasedRouter {

    /**
     * Classifies the task via the classifier ChatClient and routes it to the
     * appropriate specialist prompt.
     *
     * @param classifier  ChatClient used to classify the task (returns a category label)
     * @param specialist  ChatClient used to handle the routed task
     * @param task        the raw user task
     * @return the specialist's response
     */
    public static String route(ChatClient classifier, ChatClient specialist, String task) {
        String classifyPrompt = "Classify the following task into exactly one category "
                + "[CODE, DATA, WRITING, OTHER]. Reply with only the category label.\nTask: " + task;

        String category = classifier.prompt()
                .user(classifyPrompt)
                .call()
                .content()
                .trim()
                .toUpperCase();

        String specialistPrompt = "You are a " + category + " specialist. "
                + "Handle the following task:\n" + task;

        return specialist.prompt()
                .user(specialistPrompt)
                .call()
                .content();
    }
}
