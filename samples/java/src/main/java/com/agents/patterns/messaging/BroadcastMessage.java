package com.agents.patterns.messaging;

import org.springframework.ai.chat.client.ChatClient;

import java.util.ArrayList;
import java.util.List;

/**
 * Pattern: Broadcast Message
 * One agent broadcasts a message to all subscribers.
 * Each subscriber (ChatClient) receives the message from its own perspective.
 */
public class BroadcastMessage {

    /**
     * Broadcasts a message to all subscribers and collects their responses.
     *
     * @param chatClient  the ChatClient used to contact all subscribers
     * @param message     the broadcast message
     * @param subscribers list of subscriber names/roles
     * @return list of responses, one per subscriber
     */
    public static List<String> broadcast(ChatClient chatClient, String message,
                                         List<String> subscribers) {
        List<String> responses = new ArrayList<>();
        for (String subscriber : subscribers) {
            String prompt = "You are the " + subscriber + " agent. "
                    + "You received the following broadcast: " + message
                    + "\nRespond from your perspective.";
            String response = chatClient.prompt()
                    .user(prompt)
                    .call()
                    .content();
            responses.add(response);
        }
        return responses;
    }
}
