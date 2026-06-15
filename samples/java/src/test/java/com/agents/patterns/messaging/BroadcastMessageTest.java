package com.agents.patterns.messaging;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.ai.chat.client.ChatClient;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class BroadcastMessageTest {

    @Mock ChatClient chatClient;
    @Mock ChatClient.ChatClientRequestSpec requestSpec;
    @Mock ChatClient.CallResponseSpec callSpec;

    @Test
    void broadcast_callsEachSubscriberAndCollectsResponses() {
        when(chatClient.prompt()).thenReturn(requestSpec);
        when(requestSpec.user(anyString())).thenReturn(requestSpec);
        when(requestSpec.call()).thenReturn(callSpec);
        when(callSpec.content()).thenReturn("Acknowledged");

        List<String> subscribers = List.of("Sales", "Support", "Engineering");
        List<String> results = BroadcastMessage.broadcast(chatClient, "System shutdown at 18:00", subscribers);

        assertThat(results).hasSize(3);
        assertThat(results).allMatch(r -> r.equals("Acknowledged"));
        verify(chatClient, times(3)).prompt();
    }
}
