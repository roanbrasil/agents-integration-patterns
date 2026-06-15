package com.agents.patterns.coordination;

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
class SupervisedDelegationTest {

    @Mock ChatClient supervisor;
    @Mock ChatClient worker1;
    @Mock ChatClient worker2;
    @Mock ChatClient.ChatClientRequestSpec supSpec, w1Spec, w2Spec;
    @Mock ChatClient.CallResponseSpec supCall, w1Call, w2Call;

    @Test
    void supervise_delegatesAndReviews() {
        when(supervisor.prompt()).thenReturn(supSpec);
        when(supSpec.user(anyString())).thenReturn(supSpec);
        when(supSpec.call()).thenReturn(supCall);
        when(supCall.content())
                .thenReturn("Gather requirements\nImplement solution")
                .thenReturn("Final approved output.");

        when(worker1.prompt()).thenReturn(w1Spec);
        when(w1Spec.user(anyString())).thenReturn(w1Spec);
        when(w1Spec.call()).thenReturn(w1Call);
        when(w1Call.content()).thenReturn("Requirements gathered.");

        when(worker2.prompt()).thenReturn(w2Spec);
        when(w2Spec.user(anyString())).thenReturn(w2Spec);
        when(w2Spec.call()).thenReturn(w2Call);
        when(w2Call.content()).thenReturn("Solution implemented.");

        String result = SupervisedDelegation.supervise(supervisor,
                List.of(worker1, worker2), "Build a REST API");

        assertThat(result).isEqualTo("Final approved output.");
        verify(supervisor, times(2)).prompt();
        verify(worker1).prompt();
        verify(worker2).prompt();
    }
}
