package com.agents.patterns.context;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Pattern: Tool Provider
 * Maintains a catalogue of named tools an agent can invoke.
 * Agents discover available tools, then call them by name with arguments.
 */
public class ToolProvider {

    public record Tool(String name, String description) {}

    private final Map<String, Tool> tools = new HashMap<>();
    private final Map<String, java.util.function.Function<String, String>> handlers = new HashMap<>();

    /**
     * Registers a tool along with its execution handler.
     *
     * @param tool    the tool descriptor
     * @param handler a function that receives args and returns a result
     */
    public void registerTool(Tool tool, java.util.function.Function<String, String> handler) {
        tools.put(tool.name(), tool);
        handlers.put(tool.name(), handler);
    }

    /**
     * Lists all registered tools.
     *
     * @return immutable list of registered Tool records
     */
    public List<Tool> listTools() {
        return List.copyOf(tools.values());
    }

    /**
     * Invokes a registered tool by name.
     *
     * @param name the tool name
     * @param args the argument string to pass to the handler
     * @return the tool's result
     * @throws IllegalArgumentException if the tool is not registered
     */
    public String callTool(String name, String args) {
        if (!handlers.containsKey(name)) {
            throw new IllegalArgumentException("Unknown tool: " + name);
        }
        return handlers.get(name).apply(args);
    }
}
