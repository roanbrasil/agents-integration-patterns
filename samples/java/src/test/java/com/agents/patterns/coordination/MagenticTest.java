package com.agents.patterns.coordination;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.ai.chat.client.ChatClient;
import java.util.*;
import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;
@ExtendWith(MockitoExtension.class)
class MagenticTest {
    @Mock ChatClient chatClient;
    @Mock ChatClient.ChatClientRequestSpec requestSpec;
    @Mock ChatClient.CallResponseSpec callSpec;
    @Test void cleanCompletion() {
        Set<String> done = new HashSet<>();
        var mgr = new Magentic(ledger -> {
            if (!done.contains("researcher: market")) return List.of("researcher: market");
            if (!done.contains("writer: analysis")) return List.of("writer: analysis");
            return List.of();
        }, 8, 2)
            .register("researcher", t -> { done.add("researcher: market"); return "found info"; })
            .register("writer", t -> { done.add("writer: analysis"); return "wrote section"; });
        var ledger = mgr.run("analysis");
        assertThat(ledger.done()).hasSize(2);
        assertThat(ledger.openQuestions()).isEmpty();
    }
    @Test void stallDetection() {
        var mgr = new Magentic(l -> List.of("ghost: step"), 10, 2);
        var ledger = mgr.run("impossible");
        assertThat(ledger.openQuestions()).anyMatch(q -> q.contains("stalled"));
        assertThat(ledger.done()).isEmpty();
    }
    @Test void roundCap() {
        int[] calls = {0};
        var mgr = new Magentic(l -> List.of("worker: step"), 3, 99).register("worker", t -> { calls[0]++; return "ok"; });
        var ledger = mgr.run("endless");
        assertThat(calls[0]).isEqualTo(3);
        assertThat(ledger.openQuestions()).anyMatch(q -> q.contains("round cap"));
    }
    @Test void runWithLlmCallsClient() {
        when(chatClient.prompt()).thenReturn(requestSpec);
        when(requestSpec.user(anyString())).thenReturn(requestSpec);
        when(requestSpec.call()).thenReturn(callSpec);
        when(callSpec.content()).thenReturn("DONE");
        var ledger = Magentic.runWithLlm(chatClient, "test goal");
        assertThat(ledger).isNotNull();
    }
}
