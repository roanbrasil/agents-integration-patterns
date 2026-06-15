package com.agents.patterns.routing;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.ai.chat.client.ChatClient;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ContentBasedRouterTest {

    @Mock ChatClient classifier;
    @Mock ChatClient specialist;
    @Mock ChatClient.ChatClientRequestSpec classifierSpec;
    @Mock ChatClient.CallResponseSpec classifierCallSpec;
    @Mock ChatClient.ChatClientRequestSpec specialistSpec;
    @Mock ChatClient.CallResponseSpec specialistCallSpec;

    @Test
    void route_classifiesTaskAndForwardsToSpecialist() {
        when(classifier.prompt()).thenReturn(classifierSpec);
        when(classifierSpec.user(anyString())).thenReturn(classifierSpec);
        when(classifierSpec.call()).thenReturn(classifierCallSpec);
        when(classifierCallSpec.content()).thenReturn("CODE");

        when(specialist.prompt()).thenReturn(specialistSpec);
        when(specialistSpec.user(anyString())).thenReturn(specialistSpec);
        when(specialistSpec.call()).thenReturn(specialistCallSpec);
        when(specialistCallSpec.content()).thenReturn("Here is the code: int x = 42;");

        String result = ContentBasedRouter.route(classifier, specialist, "Write a Java hello world");

        assertThat(result).contains("int x = 42;");
    }
}
