package com.agents.patterns.messaging;

import org.springframework.ai.chat.client.ChatClient;

import java.util.HashMap;
import java.util.Map;

/**
 * Pattern: Blackboard
 * Agents share a common data store (the blackboard) to read and write intermediate results.
 * Each agent reads the current board state, contributes its output, and writes it back.
 */
public class Blackboard {

    private final Map<String, String> board = new HashMap<>();

    public void writeToBoard(String key, String value) {
        board.put(key, value);
    }

    public String readFromBoard(String key) {
        return board.get(key);
    }

    /**
     * An agent reads existing context from the blackboard, processes it via LLM,
     * and writes the result back under the given key.
     *
     * @param chatClient the agent's ChatClient
     * @param key        the key under which the result will be stored
     * @param context    the current blackboard context to include in the prompt
     * @return the agent's contribution written to the board
     */
    public String agentContribute(ChatClient chatClient, String key, String context) {
        String prompt = "Current blackboard state:\n" + context
                + "\nAs the " + key + " agent, provide your analysis or contribution.";
        String result = chatClient.prompt()
                .user(prompt)
                .call()
                .content();
        writeToBoard(key, result);
        return result;
    }
}
