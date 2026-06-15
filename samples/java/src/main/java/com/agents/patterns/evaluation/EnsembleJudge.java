package com.agents.patterns.evaluation;

import org.springframework.ai.chat.client.ChatClient;

import java.util.List;

/**
 * Pattern: Ensemble Judge
 * Multiple independent judge LLMs each evaluate the same output.
 * The final verdict is decided by majority vote. This reduces single-judge bias
 * and increases confidence in the evaluation result.
 */
public class EnsembleJudge {

    public record EnsembleResult(String finalVerdict, int approvals, int total) {}

    /**
     * Collects verdicts from all judge LLMs and returns the majority decision.
     *
     * @param judges  list of judge ChatClients
     * @param output  the agent output to evaluate
     * @param task    the original task description (for context)
     * @return an EnsembleResult with the final verdict and vote counts
     */
    public static EnsembleResult evaluate(List<ChatClient> judges, String output, String task) {
        int approvals = 0;

        for (int i = 0; i < judges.size(); i++) {
            String judgePrompt = "You are Judge " + (i + 1) + ". Evaluate this output for task: "
                    + task + "\nOutput: " + output
                    + "\nReply with exactly one word: APPROVED or REJECTED.";
            String verdict = judges.get(i).prompt()
                    .user(judgePrompt)
                    .call()
                    .content()
                    .trim()
                    .toUpperCase();

            if (verdict.contains("APPROVED")) {
                approvals++;
            }
        }

        int total = judges.size();
        String finalVerdict = (approvals > total / 2) ? "APPROVED" : "REJECTED";
        return new EnsembleResult(finalVerdict, approvals, total);
    }
}
