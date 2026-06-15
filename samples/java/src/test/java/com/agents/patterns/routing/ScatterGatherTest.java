package com.agents.patterns.routing;

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
class ScatterGatherTest {

    @Mock ChatClient agent1;
    @Mock ChatClient agent2;
    @Mock ChatClient agent3;
    @Mock ChatClient aggregator;
    @Mock ChatClient.ChatClientRequestSpec spec1, spec2, spec3, aggSpec;
    @Mock ChatClient.CallResponseSpec call1, call2, call3, aggCall;

    @Test
    void scatterGather_collectsAndAggregatesResponses() {
        when(agent1.prompt()).thenReturn(spec1);
        when(spec1.user(anyString())).thenReturn(spec1);
        when(spec1.call()).thenReturn(call1);
        when(call1.content()).thenReturn("Answer from agent 1");

        when(agent2.prompt()).thenReturn(spec2);
        when(spec2.user(anyString())).thenReturn(spec2);
        when(spec2.call()).thenReturn(call2);
        when(call2.content()).thenReturn("Answer from agent 2");

        when(agent3.prompt()).thenReturn(spec3);
        when(spec3.user(anyString())).thenReturn(spec3);
        when(spec3.call()).thenReturn(call3);
        when(call3.content()).thenReturn("Answer from agent 3");

        when(aggregator.prompt()).thenReturn(aggSpec);
        when(aggSpec.user(anyString())).thenReturn(aggSpec);
        when(aggSpec.call()).thenReturn(aggCall);
        when(aggCall.content()).thenReturn("Synthesized final answer.");

        String result = ScatterGather.scatterGather(
                List.of(agent1, agent2, agent3), aggregator, "What is AI?");

        assertThat(result).isEqualTo("Synthesized final answer.");
    }
}
