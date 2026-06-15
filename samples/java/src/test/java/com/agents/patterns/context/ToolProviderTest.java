package com.agents.patterns.context;

import com.agents.patterns.context.ToolProvider.Tool;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@ExtendWith(MockitoExtension.class)
class ToolProviderTest {

    @Test
    void toolProvider_listAndCallRegisteredTools() {
        ToolProvider provider = new ToolProvider();
        provider.registerTool(new Tool("weather", "Get current weather for a city"),
                args -> "Sunny, 25C in " + args);
        provider.registerTool(new Tool("calculator", "Evaluate a math expression"),
                args -> "Result: 42");

        assertThat(provider.listTools()).hasSize(2);
        assertThat(provider.listTools())
                .extracting(Tool::name)
                .containsExactlyInAnyOrder("weather", "calculator");

        String weatherResult = provider.callTool("weather", "London");
        assertThat(weatherResult).contains("Sunny").contains("London");
    }

    @Test
    void toolProvider_throwsForUnknownTool() {
        ToolProvider provider = new ToolProvider();
        assertThatThrownBy(() -> provider.callTool("unknown-tool", "args"))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("Unknown tool");
    }
}
