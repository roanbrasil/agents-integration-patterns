package com.agents.patterns.coordination;

import org.springframework.ai.chat.client.ChatClient;

import java.util.ArrayList;
import java.util.List;

/**
 * Pattern: Choreography
 * Agents coordinate by reacting to events on a shared event bus rather than
 * being directed by a central orchestrator. Each agent publishes and consumes events.
 */
public class Choreography {

    public record Event(String type, String payload) {}

    /**
     * Runs a two-agent choreography. Agent A reacts to the initial trigger event,
     * emits a result event, and Agent B reacts to that event, completing the chain.
     *
     * @param agentA ChatClient for the first reactive agent
     * @param agentB ChatClient for the second reactive agent
     * @return ordered list of all events produced during choreography
     */
    public static List<Event> runChoreography(ChatClient agentA, ChatClient agentB) {
        List<Event> eventBus = new ArrayList<>();

        // Seed: trigger event
        eventBus.add(new Event("ORDER_RECEIVED", "Order #1001 for 3 items"));

        // Agent A reacts to ORDER_RECEIVED
        Event trigger = eventBus.get(0);
        String aResponse = agentA.prompt()
                .user("React to event [" + trigger.type() + "]: " + trigger.payload())
                .call()
                .content();
        eventBus.add(new Event("PAYMENT_PROCESSED", aResponse));

        // Agent B reacts to PAYMENT_PROCESSED
        Event paymentEvent = eventBus.get(1);
        String bResponse = agentB.prompt()
                .user("React to event [" + paymentEvent.type() + "]: " + paymentEvent.payload())
                .call()
                .content();
        eventBus.add(new Event("SHIPMENT_DISPATCHED", bResponse));

        return eventBus;
    }
}
