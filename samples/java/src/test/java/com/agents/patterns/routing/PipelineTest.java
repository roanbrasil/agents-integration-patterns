package com.agents.patterns.routing;

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
class PipelineTest {

    @Mock ChatClient planner;
    @Mock ChatClient executor;
    @Mock ChatClient verifier;
    @Mock ChatClient.ChatClientRequestSpec planSpec, execSpec, verSpec;
    @Mock ChatClient.CallResponseSpec planCall, execCall, verCall;

    @Test
    void pipeline_chainsStateSequentially() {
        when(planner.prompt()).thenReturn(planSpec);
        when(planSpec.user(anyString())).thenReturn(planSpec);
        when(planSpec.call()).thenReturn(planCall);
        when(planCall.content()).thenReturn("Step 1: gather data. Step 2: analyse.");

        when(executor.prompt()).thenReturn(execSpec);
        when(execSpec.user(anyString())).thenReturn(execSpec);
        when(execSpec.call()).thenReturn(execCall);
        when(execCall.content()).thenReturn("Data gathered and analysed successfully.");

        when(verifier.prompt()).thenReturn(verSpec);
        when(verSpec.user(anyString())).thenReturn(verSpec);
        when(verSpec.call()).thenReturn(verCall);
        when(verCall.content()).thenReturn("Verified: output is correct.");

        ArgumentCaptor<String> execCaptor = ArgumentCaptor.forClass(String.class);
        ArgumentCaptor<String> verCaptor  = ArgumentCaptor.forClass(String.class);

        String result = Pipeline.pipeline(planner, executor, verifier, "Analyse sales data");

        verify(execSpec).user(execCaptor.capture());
        verify(verSpec).user(verCaptor.capture());

        assertThat(execCaptor.getValue()).contains("Step 1: gather data");
        assertThat(verCaptor.getValue()).contains("Data gathered and analysed");
        assertThat(result).isEqualTo("Verified: output is correct.");
    }
}
