package com.agents.patterns.resilience;

import org.springframework.ai.chat.client.ChatClient;

/**
 * Pattern: Circuit Breaker
 * Tracks consecutive failures. After reaching the threshold the circuit moves to OPEN
 * and all calls are rejected immediately. After a reset the circuit becomes HALF_OPEN,
 * allowing one probe call. Success closes the circuit; failure reopens it.
 */
public class CircuitBreaker {

    public enum State { CLOSED, OPEN, HALF_OPEN }

    public static class CircuitOpenException extends RuntimeException {
        public CircuitOpenException(String msg) { super(msg); }
    }

    private State state = State.CLOSED;
    private int failureCount = 0;
    private final int failureThreshold;

    public CircuitBreaker(int failureThreshold) {
        this.failureThreshold = failureThreshold;
    }

    public State getState() { return state; }

    /**
     * Calls the agent if the circuit is CLOSED or HALF_OPEN.
     * Throws CircuitOpenException when OPEN.
     */
    public String call(ChatClient agent, String task) {
        if (state == State.OPEN) {
            throw new CircuitOpenException("Circuit is OPEN — call rejected for task: " + task);
        }
        try {
            String result = agent.prompt().user(task).call().content();
            onSuccess();
            return result;
        } catch (Exception e) {
            onFailure();
            throw e;
        }
    }

    /** Transition to HALF_OPEN to allow a probe after the circuit was OPEN. */
    public void attemptReset() {
        state = State.HALF_OPEN;
    }

    private void onSuccess() {
        failureCount = 0;
        state = State.CLOSED;
    }

    private void onFailure() {
        failureCount++;
        if (failureCount >= failureThreshold) {
            state = State.OPEN;
        }
    }
}
