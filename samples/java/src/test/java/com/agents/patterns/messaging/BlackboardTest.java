package com.agents.patterns.messaging;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.ai.chat.client.ChatClient;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class BlackboardTest {

    @Mock ChatClient chatClient;
    @Mock ChatClient.ChatClientRequestSpec requestSpec;
    @Mock ChatClient.CallResponseSpec callSpec;

    @Test
    void blackboard_writeReadAndAgentContribute() {
        Blackboard blackboard = new Blackboard();
        blackboard.writeToBoard("initial", "Problem: optimize query performance");
        assertThat(blackboard.readFromBoard("initial")).contains("optimize");

        when(chatClient.prompt()).thenReturn(requestSpec);
        when(requestSpec.user(anyString())).thenReturn(requestSpec);
        when(requestSpec.call()).thenReturn(callSpec);
        when(callSpec.content()).thenReturn("Add an index on the user_id column.");

        String contribution = blackboard.agentContribute(chatClient, "db-agent",
                blackboard.readFromBoard("initial"));

        assertThat(contribution).isEqualTo("Add an index on the user_id column.");
        assertThat(blackboard.readFromBoard("db-agent")).isEqualTo(contribution);
    }
}
