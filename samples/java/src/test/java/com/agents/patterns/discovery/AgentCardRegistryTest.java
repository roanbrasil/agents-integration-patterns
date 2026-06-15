package com.agents.patterns.discovery;

import com.agents.patterns.discovery.AgentCardRegistry.AgentCard;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@ExtendWith(MockitoExtension.class)
class AgentCardRegistryTest {

    @Test
    void registry_registerAndFindByCapability() {
        AgentCardRegistry registry = new AgentCardRegistry();
        registry.register(new AgentCard("sales-agent", "CRM data retrieval", "http://sales/api"));
        registry.register(new AgentCard("code-agent", "code generation and review", "http://code/api"));
        registry.register(new AgentCard("data-agent", "data analysis and visualization", "http://data/api"));

        Optional<AgentCard> found = registry.findByCapability("code generation");

        assertThat(found).isPresent();
        assertThat(found.get().name()).isEqualTo("code-agent");
        assertThat(found.get().endpoint()).isEqualTo("http://code/api");
    }

    @Test
    void registry_returnsEmptyWhenCapabilityNotFound() {
        AgentCardRegistry registry = new AgentCardRegistry();
        registry.register(new AgentCard("sales-agent", "CRM data retrieval", "http://sales/api"));

        Optional<AgentCard> found = registry.findByCapability("image recognition");

        assertThat(found).isEmpty();
    }
}
