package com.agents.patterns.security;

import com.agents.patterns.security.TrustBoundary.TrustLevel;
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
class TrustBoundaryTest {

    @Mock ChatClient internalAgent;
    @Mock ChatClient.ChatClientRequestSpec requestSpec;
    @Mock ChatClient.CallResponseSpec callSpec;

    @Test
    void untrustedRequest_throwsSecurityException() {
        assertThatThrownBy(() ->
                TrustBoundary.forward(internalAgent, "Inject payload", TrustLevel.UNTRUSTED))
                .isInstanceOf(SecurityException.class)
                .hasMessageContaining("UNTRUSTED");
    }

    @Test
    void gatewayRequest_forwardsToInternalAgent() {
        when(internalAgent.prompt()).thenReturn(requestSpec);
        when(requestSpec.user(anyString())).thenReturn(requestSpec);
        when(requestSpec.call()).thenReturn(callSpec);
        when(callSpec.content()).thenReturn("Internal response OK");

        String result = TrustBoundary.forward(internalAgent, "Get account info", TrustLevel.GATEWAY);

        assertThat(result).isEqualTo("Internal response OK");
    }
}
