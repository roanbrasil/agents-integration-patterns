package com.agents.patterns.coordination;

import org.springframework.ai.chat.client.ChatClient;

import java.util.Map;

/**
 * Pattern: Peer-to-Peer Delegation
 * An agent dynamically discovers a capable peer from a pool and delegates a task
 * to it without a central coordinator. Peer discovery is driven by capability matching.
 */
public class PeerToPeerDelegation {

    /**
     * Looks up the first agent in the pool whose key contains the required capability
     * (case-insensitive) and delegates the task to it.
     *
     * @param agentPool          map of capability-label → ChatClient
     * @param requiredCapability the capability the requester needs
     * @param task               the task to delegate
     * @return the chosen peer's response
     * @throws IllegalStateException if no peer with the required capability is found
     */
    public static String delegate(Map<String, ChatClient> agentPool,
                                  String requiredCapability,
                                  String task) {
        ChatClient peer = agentPool.entrySet().stream()
                .filter(e -> e.getKey().toLowerCase().contains(requiredCapability.toLowerCase()))
                .map(Map.Entry::getValue)
                .findFirst()
                .orElseThrow(() -> new IllegalStateException(
                        "No peer found for capability: " + requiredCapability));

        return peer.prompt()
                .user("You were selected because you have the capability: "
                        + requiredCapability + "\nPlease complete: " + task)
                .call()
                .content();
    }
}
