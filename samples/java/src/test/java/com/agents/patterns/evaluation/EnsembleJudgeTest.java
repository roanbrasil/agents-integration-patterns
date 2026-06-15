package com.agents.patterns.evaluation;

import com.agents.patterns.evaluation.EnsembleJudge.EnsembleResult;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.ai.chat.client.ChatClient;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class EnsembleJudgeTest {

    @Mock ChatClient judge1, judge2, judge3;
    @Mock ChatClient.ChatClientRequestSpec spec1, spec2, spec3;
    @Mock ChatClient.CallResponseSpec call1, call2, call3;

    @Test
    void evaluate_majorityApprovedWins() {
        when(judge1.prompt()).thenReturn(spec1);
        when(spec1.user(anyString())).thenReturn(spec1);
        when(spec1.call()).thenReturn(call1);
        when(call1.content()).thenReturn("APPROVED");

        when(judge2.prompt()).thenReturn(spec2);
        when(spec2.user(anyString())).thenReturn(spec2);
        when(spec2.call()).thenReturn(call2);
        when(call2.content()).thenReturn("APPROVED");

        when(judge3.prompt()).thenReturn(spec3);
        when(spec3.user(anyString())).thenReturn(spec3);
        when(spec3.call()).thenReturn(call3);
        when(call3.content()).thenReturn("REJECTED");

        EnsembleResult result = EnsembleJudge.evaluate(
                List.of(judge1, judge2, judge3),
                "The output text here",
                "Summarise the report");

        assertThat(result.finalVerdict()).isEqualTo("APPROVED");
        assertThat(result.approvals()).isEqualTo(2);
        assertThat(result.total()).isEqualTo(3);
    }

    @Test
    void evaluate_majorityRejectedWins() {
        when(judge1.prompt()).thenReturn(spec1);
        when(spec1.user(anyString())).thenReturn(spec1);
        when(spec1.call()).thenReturn(call1);
        when(call1.content()).thenReturn("REJECTED");

        when(judge2.prompt()).thenReturn(spec2);
        when(spec2.user(anyString())).thenReturn(spec2);
        when(spec2.call()).thenReturn(call2);
        when(call2.content()).thenReturn("REJECTED");

        when(judge3.prompt()).thenReturn(spec3);
        when(spec3.user(anyString())).thenReturn(spec3);
        when(spec3.call()).thenReturn(call3);
        when(call3.content()).thenReturn("APPROVED");

        EnsembleResult result = EnsembleJudge.evaluate(
                List.of(judge1, judge2, judge3),
                "Poor quality output",
                "Summarise the report");

        assertThat(result.finalVerdict()).isEqualTo("REJECTED");
        assertThat(result.approvals()).isEqualTo(1);
        assertThat(result.total()).isEqualTo(3);
    }
}
