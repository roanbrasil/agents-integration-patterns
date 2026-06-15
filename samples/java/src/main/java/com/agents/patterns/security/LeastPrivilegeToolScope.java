package com.agents.patterns.security;

import java.util.Set;
import java.util.function.Function;
import java.util.HashMap;
import java.util.Map;

/**
 * Pattern: Least-Privilege Tool Scope
 * Each agent is given a scoped tool server that exposes only the tools it needs.
 * Attempts to call tools outside the allowed set throw a SecurityException,
 * enforcing the principle of least privilege.
 */
public class LeastPrivilegeToolScope {

    private final Set<String> allowedTools;
    private final Map<String, Function<String, String>> toolHandlers = new HashMap<>();

    public LeastPrivilegeToolScope(Set<String> allowedTools) {
        this.allowedTools = Set.copyOf(allowedTools);
    }

    /**
     * Registers a handler for a tool. Only tools in the allowed set should be registered.
     */
    public void registerHandler(String toolName, Function<String, String> handler) {
        toolHandlers.put(toolName, handler);
    }

    /**
     * Calls the named tool with the provided arguments.
     *
     * @param toolName the name of the tool to invoke
     * @param args     the argument string
     * @return the tool's result
     * @throws SecurityException if the tool is not in the allowed set
     */
    public String callTool(String toolName, String args) {
        if (!allowedTools.contains(toolName)) {
            throw new SecurityException("Access denied: tool '" + toolName
                    + "' is outside the agent's allowed scope.");
        }
        Function<String, String> handler = toolHandlers.get(toolName);
        if (handler == null) {
            throw new IllegalStateException("No handler registered for tool: " + toolName);
        }
        return handler.apply(args);
    }
}
