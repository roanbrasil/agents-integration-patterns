package com.agents.patterns.coordination;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.ai.chat.client.ChatClient;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class OrchestratorTest {

    @Mock ChatClient step1, step2, step3;
    @Mock ChatClient.ChatClientRequestSpec s1Spec, s2Spec, s3Spec;
    @Mock ChatClient.CallResponseSpec s1Call, s2Call, s3Call;

    @Test
    void orchestrate_stateFlowsThroughSteps() {
        when(step1.prompt()).thenReturn(s1Spec);
        when(s1Spec.user(anyString())).thenReturn(s1Spec);
        when(s1Spec.call()).thenReturn(s1Call);
        when(s1Call.content()).thenReturn("Step1Output");

        when(step2.prompt()).thenReturn(s2Spec);
        when(s2Spec.user(anyString())).thenReturn(s2Spec);
        when(s2Spec.call()).thenReturn(s2Call);
        when(s2Call.content()).thenReturn("Step2Output");

        when(step3.prompt()).thenReturn(s3Spec);
        when(s3Spec.user(anyString())).thenReturn(s3Spec);
        when(s3Spec.call()).thenReturn(s3Call);
        when(s3Call.content()).thenReturn("FinalOutput");

        ArgumentCaptor<String> cap2 = ArgumentCaptor.forClass(String.class);
        ArgumentCaptor<String> cap3 = ArgumentCaptor.forClass(String.class);

        String result = Orchestrator.orchestrate(step1, step2, step3, "raw input");

        verify(s2Spec).user(cap2.capture());
        verify(s3Spec).user(cap3.capture());
        assertThat(cap2.getValue()).contains("Step1Output");
        assertThat(cap3.getValue()).contains("Step2Output");
        assertThat(result).isEqualTo("FinalOutput");
    }
}
