package com.agents.patterns.resilience;

import com.agents.patterns.resilience.CheckpointResume.Checkpoint;
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
class CheckpointResumeTest {

    @Mock ChatClient agent;
    @Mock ChatClient.ChatClientRequestSpec requestSpec;
    @Mock ChatClient.CallResponseSpec callSpec;

    @Test
    void runWithCheckpoints_checkpointsEachStep() {
        when(agent.prompt()).thenReturn(requestSpec);
        when(requestSpec.user(anyString())).thenReturn(requestSpec);
        when(requestSpec.call()).thenReturn(callSpec);
        when(callSpec.content())
                .thenReturn("Step 1 done")
                .thenReturn("Step 2 done")
                .thenReturn("Step 3 done");

        List<String> steps = List.of("Fetch data", "Transform data", "Load data");
        List<Checkpoint> checkpoints = CheckpointResume.runWithCheckpoints(agent, steps);

        assertThat(checkpoints).hasSize(3);
        assertThat(checkpoints.get(0)).isEqualTo(new Checkpoint("Fetch data", "Step 1 done"));
        assertThat(checkpoints.get(1)).isEqualTo(new Checkpoint("Transform data", "Step 2 done"));
        assertThat(checkpoints.get(2)).isEqualTo(new Checkpoint("Load data", "Step 3 done"));
        verify(agent, times(3)).prompt();
    }
}
