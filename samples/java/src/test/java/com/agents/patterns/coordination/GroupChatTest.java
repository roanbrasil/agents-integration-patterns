package com.agents.patterns.coordination;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.ai.chat.client.ChatClient;
import java.util.List;
import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;
@ExtendWith(MockitoExtension.class)
class GroupChatTest {
    @Mock ChatClient chatClient;
    @Mock ChatClient.ChatClientRequestSpec requestSpec;
    @Mock ChatClient.CallResponseSpec callSpec;
    void setupMock(String response) {
        when(chatClient.prompt()).thenReturn(requestSpec);
        when(requestSpec.user(anyString())).thenReturn(requestSpec);
        when(requestSpec.call()).thenReturn(callSpec);
        when(callSpec.content()).thenReturn(response);
    }
    @Test void threadStartsWithInput() {
        var chat = new GroupChat(GroupChat.makerCheckerManager("APPROVED"), 4)
            .add("maker", t -> "draft v1")
            .add("checker", t -> "APPROVED: good");
        var thread = chat.run("write policy");
        assertThat(thread.get(0)).isEqualTo(new GroupChat.Turn("input", "write policy"));
    }
    @Test void stopsOnApproval() {
        var chat = new GroupChat(GroupChat.makerCheckerManager("APPROVED"), 10)
            .add("maker", t -> "draft v1")
            .add("checker", t -> "APPROVED: done");
        var thread = chat.run("goal");
        assertThat(thread.get(thread.size() - 1).speaker()).isEqualTo("checker");
        assertThat(thread.get(thread.size() - 1).text()).contains("APPROVED");
    }
    @Test void iterationCapPreventsInfiniteLoop() {
        var chat = new GroupChat(GroupChat.makerCheckerManager("APPROVED"), 4)
            .add("maker", t -> "draft")
            .add("checker", t -> "REJECTED: nope");
        assertThat(chat.run("x")).hasSize(1 + 4);
    }
    @Test void runWithLlmCallsChatClient() {
        setupMock("APPROVED: looks good");
        String result = GroupChat.runWithLlm(chatClient, "refund policy");
        assertThat(result).isNotEmpty();
    }
}
