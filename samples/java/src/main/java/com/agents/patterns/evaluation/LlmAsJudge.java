package com.agents.patterns.evaluation;

import org.springframework.ai.chat.client.ChatClient;

/**
 * Pattern: LLM-as-Judge
 * A producer agent generates an output. A separate judge LLM evaluates the output
 * against the original task. If rejected, the producer retries up to a maximum number
 * of attempts, passing the judge's feedback as context for improvement.
 */
public class LlmAsJudge {

    public record JudgeResult(String output, String verdict, int retries) {}

    private static final int MAX_RETRIES = 3;

    /**
     * Runs the producer-judge loop. The producer generates output; the judge evaluates.
     * Retries on REJECTED verdict until approved or MAX_RETRIES is reached.
     *
     * @param producer ChatClient for the content-generating agent
     * @param judge    ChatClient for the evaluation agent
     * @param task     the original task description
     * @return a JudgeResult containing final output, verdict, and retry count
     */
    public static JudgeResult judge(ChatClient producer, ChatClient judge, String task) {
        String output = "";
        String verdict = "REJECTED";
        int retries = 0;
        String feedback = "";

        while (retries < MAX_RETRIES && verdict.contains("REJECTED")) {
            String producerPrompt = task
                    + (feedback.isEmpty() ? "" : "\nPrevious feedback: " + feedback);
            output = producer.prompt().user(producerPrompt).call().content();

            String judgePrompt = "Task: " + task + "\nOutput: " + output
                    + "\nReply APPROVED or REJECTED with a brief reason.";
            verdict = judge.prompt().user(judgePrompt).call().content();
            if (verdict.contains("REJECTED")) {
                feedback = verdict;
            }
            retries++;
        }

        return new JudgeResult(output, verdict, retries);
    }
}
