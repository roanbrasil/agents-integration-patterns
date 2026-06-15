package com.agents.patterns.resilience;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.ai.chat.client.ChatClient;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class DeadLetterAgentTest {

    @Mock ChatClient primaryAgent;
    @Mock ChatClient deadLetterAgent;
    @Mock ChatClient.ChatClientRequestSpec primarySpec, dlSpec;
    @Mock ChatClient.CallResponseSpec primaryCall, dlCall;

    @Test
    void process_routesToDeadLetterAfterMaxRetries() {
        when(primaryAgent.prompt()).thenReturn(primarySpec);
        when(primarySpec.user(anyString())).thenReturn(primarySpec);
        when(primarySpec.call()).thenThrow(new RuntimeException("Service unavailable"));

        when(deadLetterAgent.prompt()).thenReturn(dlSpec);
        when(dlSpec.user(anyString())).thenReturn(dlSpec);
        when(dlSpec.call()).thenReturn(dlCall);
        when(dlCall.content()).thenReturn("Task quarantined by dead-letter handler.");

        String result = DeadLetterAgent.process(primaryAgent, deadLetterAgent, "Process payment", 3);

        assertThat(result).isEqualTo("Task quarantined by dead-letter handler.");
        verify(primaryAgent, times(3)).prompt();
        verify(deadLetterAgent).prompt();
    }

    @Test
    void process_succeedsWithPrimaryAgent() {
        when(primaryAgent.prompt()).thenReturn(primarySpec);
        when(primarySpec.user(anyString())).thenReturn(primarySpec);
        when(primarySpec.call()).thenReturn(primaryCall);
        when(primaryCall.content()).thenReturn("Payment processed.");

        String result = DeadLetterAgent.process(primaryAgent, deadLetterAgent, "Process payment", 3);

        assertThat(result).isEqualTo("Payment processed.");
        verify(deadLetterAgent, times(0)).prompt();
    }
}
