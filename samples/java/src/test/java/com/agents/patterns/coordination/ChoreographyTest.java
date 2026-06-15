package com.agents.patterns.coordination;

import com.agents.patterns.coordination.Choreography.Event;
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
class ChoreographyTest {

    @Mock ChatClient agentA;
    @Mock ChatClient agentB;
    @Mock ChatClient.ChatClientRequestSpec specA, specB;
    @Mock ChatClient.CallResponseSpec callA, callB;

    @Test
    void choreography_producesEventChain() {
        when(agentA.prompt()).thenReturn(specA);
        when(specA.user(anyString())).thenReturn(specA);
        when(specA.call()).thenReturn(callA);
        when(callA.content()).thenReturn("Payment confirmed for Order #1001");

        when(agentB.prompt()).thenReturn(specB);
        when(specB.user(anyString())).thenReturn(specB);
        when(specB.call()).thenReturn(callB);
        when(callB.content()).thenReturn("Package dispatched via courier");

        List<Event> events = Choreography.runChoreography(agentA, agentB);

        assertThat(events).hasSize(3);
        assertThat(events.get(0).type()).isEqualTo("ORDER_RECEIVED");
        assertThat(events.get(1).type()).isEqualTo("PAYMENT_PROCESSED");
        assertThat(events.get(1).payload()).contains("Payment confirmed");
        assertThat(events.get(2).type()).isEqualTo("SHIPMENT_DISPATCHED");
        assertThat(events.get(2).payload()).contains("dispatched");
    }
}
