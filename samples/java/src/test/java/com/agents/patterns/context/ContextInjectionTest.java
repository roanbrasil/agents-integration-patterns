package com.agents.patterns.context;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.ai.chat.client.ChatClient;

import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ContextInjectionTest {

    @Mock ChatClient chatClient;
    @Mock ChatClient.ChatClientRequestSpec requestSpec;
    @Mock ChatClient.CallResponseSpec callSpec;

    @Test
    void injectAndQuery_buildsPromptWithContext() {
        ArgumentCaptor<String> promptCaptor = ArgumentCaptor.forClass(String.class);
        when(chatClient.prompt()).thenReturn(requestSpec);
        when(requestSpec.user(anyString())).thenReturn(requestSpec);
        when(requestSpec.call()).thenReturn(callSpec);
        when(callSpec.content()).thenReturn("Your account balance is $500.");

        Map<String, String> ctx = Map.of("user", "Alice", "plan", "Premium");
        String result = ContextInjection.injectAndQuery(chatClient, ctx, "What is my balance?");

        verify(requestSpec).user(promptCaptor.capture());
        assertThat(promptCaptor.getValue()).contains("user: Alice");
        assertThat(promptCaptor.getValue()).contains("plan: Premium");
        assertThat(promptCaptor.getValue()).contains("What is my balance?");
        assertThat(result).isEqualTo("Your account balance is $500.");
    }
}
