package com.agents.patterns.resilience;

import com.agents.patterns.resilience.CircuitBreaker.CircuitOpenException;
import com.agents.patterns.resilience.CircuitBreaker.State;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.ai.chat.client.ChatClient;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class CircuitBreakerTest {

    @Mock ChatClient agent;
    @Mock ChatClient.ChatClientRequestSpec requestSpec;
    @Mock ChatClient.CallResponseSpec callSpec;

    @Test
    void circuitBreaker_opensAfterThresholdFailures() {
        when(agent.prompt()).thenReturn(requestSpec);
        when(requestSpec.user(anyString())).thenReturn(requestSpec);
        when(requestSpec.call()).thenThrow(new RuntimeException("backend down"));

        CircuitBreaker cb = new CircuitBreaker(2);
        assertThat(cb.getState()).isEqualTo(State.CLOSED);

        assertThatThrownBy(() -> cb.call(agent, "task")).isInstanceOf(RuntimeException.class);
        assertThat(cb.getState()).isEqualTo(State.CLOSED);

        assertThatThrownBy(() -> cb.call(agent, "task")).isInstanceOf(RuntimeException.class);
        assertThat(cb.getState()).isEqualTo(State.OPEN);

        assertThatThrownBy(() -> cb.call(agent, "task")).isInstanceOf(CircuitOpenException.class);
    }

    @Test
    void circuitBreaker_closesAfterSuccessfulProbe() {
        when(agent.prompt()).thenReturn(requestSpec);
        when(requestSpec.user(anyString())).thenReturn(requestSpec);
        when(requestSpec.call()).thenReturn(callSpec);
        when(callSpec.content()).thenReturn("OK");

        CircuitBreaker cb = new CircuitBreaker(2);
        cb.attemptReset();
        assertThat(cb.getState()).isEqualTo(State.HALF_OPEN);

        String result = cb.call(agent, "probe task");

        assertThat(result).isEqualTo("OK");
        assertThat(cb.getState()).isEqualTo(State.CLOSED);
    }
}
