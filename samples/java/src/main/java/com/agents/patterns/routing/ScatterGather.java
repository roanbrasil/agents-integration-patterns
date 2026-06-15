package com.agents.patterns.routing;

import org.springframework.ai.chat.client.ChatClient;

import java.util.List;
import java.util.StringJoiner;

/**
 * Pattern: Scatter-Gather
 * A question is scattered to multiple specialist agents in parallel (here sequentially
 * for simplicity). All individual responses are then gathered and passed to an
 * aggregator agent that synthesises a final answer.
 */
public class ScatterGather {

    /**
     * Sends the question to every agent in the pool, collects their answers,
     * then asks the aggregator to produce a unified response.
     *
     * @param agents     list of specialist ChatClients
     * @param aggregator ChatClient that synthesises all partial answers
     * @param question   the question to scatter
     * @return the aggregated final answer
     */
    public static String scatterGather(List<ChatClient> agents,
                                       ChatClient aggregator,
                                       String question) {
        StringJoiner gathered = new StringJoiner("\n---\n", "Individual agent responses:\n", "");

        for (int i = 0; i < agents.size(); i++) {
            String agentPrompt = "Agent " + (i + 1) + ", answer this question: " + question;
            String response = agents.get(i).prompt()
                    .user(agentPrompt)
                    .call()
                    .content();
            gathered.add("Agent " + (i + 1) + ": " + response);
        }

        String aggregatePrompt = gathered + "\n\nSynthesize these responses into one final answer.";
        return aggregator.prompt()
                .user(aggregatePrompt)
                .call()
                .content();
    }
}
