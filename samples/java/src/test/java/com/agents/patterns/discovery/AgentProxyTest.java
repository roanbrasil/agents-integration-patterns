package com.agents.patterns.discovery;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.ai.chat.client.ChatClient;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class AgentProxyTest {

    @Mock ChatClient backend;
    @Mock ChatClient.ChatClientRequestSpec requestSpec;
    @Mock ChatClient.CallResponseSpec callSpec;

    @Test
    void proxy_callsBackendAndReturnsResult() {
        when(backend.prompt()).thenReturn(requestSpec);
        when(requestSpec.user(anyString())).thenReturn(requestSpec);
        when(requestSpec.call()).thenReturn(callSpec);
        when(callSpec.content()).thenReturn("Backend response: task done.");

        String result = AgentProxy.proxy(backend, "Translate document to French");

        assertThat(result).isEqualTo("Backend response: task done.");
        verify(backend).prompt();
        verify(requestSpec).user("Translate document to French");
    }
}
