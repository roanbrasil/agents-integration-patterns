package com.agents.patterns.security;

import org.springframework.ai.chat.client.ChatClient;

/**
 * Pattern: Trust Boundary
 * Requests arriving from untrusted zones are rejected at the boundary.
 * Only requests from the GATEWAY or INTERNAL trust levels are forwarded
 * to internal agents, preventing prompt-injection from external sources.
 */
public class TrustBoundary {

    public enum TrustLevel { UNTRUSTED, GATEWAY, INTERNAL }

    /**
     * Evaluates the trust level of a request and forwards it to the internal agent
     * only if the trust level is sufficient.
     *
     * @param internalAgent ChatClient for the internal agent
     * @param request       the raw request content
     * @param level         the trust level of the request source
     * @return the internal agent's response
     * @throws SecurityException if the trust level is UNTRUSTED
     */
    public static String forward(ChatClient internalAgent, String request, TrustLevel level) {
        if (level == TrustLevel.UNTRUSTED) {
            throw new SecurityException(
                    "Request rejected: UNTRUSTED sources cannot access internal agents.");
        }

        String enrichedRequest = "[" + level.name() + "] " + request;
        return internalAgent.prompt()
                .user(enrichedRequest)
                .call()
                .content();
    }
}
