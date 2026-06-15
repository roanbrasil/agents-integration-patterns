package com.agents.patterns.evaluation;

import com.agents.patterns.evaluation.LlmAsJudge.JudgeResult;
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
class LlmAsJudgeTest {

    @Mock ChatClient producer;
    @Mock ChatClient judge;
    @Mock ChatClient.ChatClientRequestSpec producerSpec, judgeSpec;
    @Mock ChatClient.CallResponseSpec producerCall, judgeCall;

    @Test
    void judge_approvedOnFirstTry() {
        when(producer.prompt()).thenReturn(producerSpec);
        when(producerSpec.user(anyString())).thenReturn(producerSpec);
        when(producerSpec.call()).thenReturn(producerCall);
        when(producerCall.content()).thenReturn("Great summary produced.");

        when(judge.prompt()).thenReturn(judgeSpec);
        when(judgeSpec.user(anyString())).thenReturn(judgeSpec);
        when(judgeSpec.call()).thenReturn(judgeCall);
        when(judgeCall.content()).thenReturn("APPROVED — concise and accurate.");

        JudgeResult result = LlmAsJudge.judge(producer, judge, "Summarise the report");

        assertThat(result.verdict()).contains("APPROVED");
        assertThat(result.retries()).isEqualTo(1);
        assertThat(result.output()).isEqualTo("Great summary produced.");
    }

    @Test
    void judge_retriesOnRejectedThenApproves() {
        when(producer.prompt()).thenReturn(producerSpec);
        when(producerSpec.user(anyString())).thenReturn(producerSpec);
        when(producerSpec.call()).thenReturn(producerCall);
        when(producerCall.content()).thenReturn("Improved output");

        when(judge.prompt()).thenReturn(judgeSpec);
        when(judgeSpec.user(anyString())).thenReturn(judgeSpec);
        when(judgeSpec.call()).thenReturn(judgeCall);
        when(judgeCall.content())
                .thenReturn("REJECTED — too vague")
                .thenReturn("APPROVED — much better");

        JudgeResult result = LlmAsJudge.judge(producer, judge, "Summarise the report");

        assertThat(result.verdict()).contains("APPROVED");
        assertThat(result.retries()).isEqualTo(2);
        verify(producer, times(2)).prompt();
        verify(judge, times(2)).prompt();
    }
}
