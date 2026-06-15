package com.agents.patterns.discovery;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * Pattern: Agent Card Registry
 * Agents publish capability descriptors (AgentCards) to a central registry.
 * Other agents discover suitable peers by querying the registry.
 */
public class AgentCardRegistry {

    public record AgentCard(String name, String capability, String endpoint) {}

    private final List<AgentCard> registry = new ArrayList<>();

    /**
     * Registers an AgentCard in the discovery registry.
     *
     * @param card the agent card to register
     */
    public void register(AgentCard card) {
        registry.add(card);
    }

    /**
     * Finds the first registered agent that matches the requested capability.
     *
     * @param capability the capability to search for (case-insensitive substring match)
     * @return an Optional containing the matched AgentCard, or empty if not found
     */
    public Optional<AgentCard> findByCapability(String capability) {
        return registry.stream()
                .filter(c -> c.capability().toLowerCase().contains(capability.toLowerCase()))
                .findFirst();
    }

    /**
     * Returns all registered agent cards.
     */
    public List<AgentCard> listAll() {
        return List.copyOf(registry);
    }
}
