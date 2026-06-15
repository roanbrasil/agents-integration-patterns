package com.agents.patterns.discovery;

import org.springframework.ai.chat.client.ChatClient;

import java.util.logging.Logger;

/**
 * Pattern: Agent Proxy
 * A proxy wraps a backend ChatClient agent, adding cross-cutting concerns
 * such as logging, latency measurement, and input/output validation
 * without modifying the underlying agent.
 */
public class AgentProxy {

    private static final Logger log = Logger.getLogger(AgentProxy.class.getName());

    /**
     * Proxies a task to the backend agent while adding logging and timing.
     *
     * @param backend the real ChatClient agent to delegate to
     * @param task    the task to forward
     * @return the backend agent's response
     */
    public static String proxy(ChatClient backend, String task) {
        log.info("[PROXY] Forwarding task: " + task);
        long start = System.currentTimeMillis();

        String result = backend.prompt()
                .user(task)
                .call()
                .content();

        long elapsed = System.currentTimeMillis() - start;
        log.info("[PROXY] Response received in " + elapsed + "ms: " + result);
        return result;
    }
}
