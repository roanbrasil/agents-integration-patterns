package com.agents.patterns.context;

import org.springframework.ai.chat.client.ChatClient;

import java.util.Map;

/**
 * Pattern: Context Injection
 * Enriches an agent's prompt with structured context (user data, session state,
 * domain facts) before sending the user's question. Prevents the agent from
 * having to retrieve context itself and keeps prompts reproducible.
 */
public class ContextInjection {

    /**
     * Assembles context entries into a system preamble, appends the user question,
     * and calls the agent.
     *
     * @param chatClient the agent ChatClient
     * @param context    key-value pairs of contextual information
     * @param question   the user's question
     * @return the agent's response
     */
    public static String injectAndQuery(ChatClient chatClient,
                                        Map<String, String> context,
                                        String question) {
        StringBuilder sb = new StringBuilder("Context:\n");
        context.forEach((k, v) -> sb.append("- ").append(k).append(": ").append(v).append("\n"));
        sb.append("\nQuestion: ").append(question);

        return chatClient.prompt()
                .user(sb.toString())
                .call()
                .content();
    }
}
