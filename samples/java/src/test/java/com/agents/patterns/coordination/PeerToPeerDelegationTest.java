package com.agents.patterns.coordination;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.ai.chat.client.ChatClient;

import java.util.LinkedHashMap;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class PeerToPeerDelegationTest {

    @Mock ChatClient translationAgent;
    @Mock ChatClient.ChatClientRequestSpec requestSpec;
    @Mock ChatClient.CallResponseSpec callSpec;

    @Test
    void delegate_discoversAndDelegatesToCapablePeer() {
        when(translationAgent.prompt()).thenReturn(requestSpec);
        when(requestSpec.user(anyString())).thenReturn(requestSpec);
        when(requestSpec.call()).thenReturn(callSpec);
        when(callSpec.content()).thenReturn("Translated: Bonjour le monde");

        Map<String, ChatClient> pool = new LinkedHashMap<>();
        pool.put("translation-service", translationAgent);
        pool.put("image-recognition-service", null);

        String result = PeerToPeerDelegation.delegate(pool, "translation", "Translate 'Hello World' to French");

        assertThat(result).isEqualTo("Translated: Bonjour le monde");
    }

    @Test
    void delegate_throwsWhenCapabilityNotFound() {
        Map<String, ChatClient> pool = Map.of("weather-service", translationAgent);
        assertThatThrownBy(() -> PeerToPeerDelegation.delegate(pool, "translation", "Translate text"))
                .isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("translation");
    }
}
