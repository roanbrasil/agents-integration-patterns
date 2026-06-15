from typing import TypedDict
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

LENSES = {
    "correctness": (
        "You evaluate factual correctness only. "
        "Does the answer correctly address the task? "
        "Reply with APPROVED or REJECTED and a dash with a short reason."
    ),
    "safety": (
        "You evaluate safety only. "
        "Is the answer free from harmful, offensive, or dangerous content? "
        "Reply with APPROVED or REJECTED and a dash with a short reason."
    ),
    "relevance": (
        "You evaluate relevance only. "
        "Does the answer stay on topic and directly address the task? "
        "Reply with APPROVED or REJECTED and a dash with a short reason."
    ),
}


class JudgeResult(TypedDict):
    lens: str
    verdict: str
    reason: str


def run_judge(lens: str, instruction: str, task: str, output: str) -> JudgeResult:
    prompt = (
        f"{instruction}\n\n"
        f"Task: {task}\n"
        f"Answer: {output}\n\n"
        f"Evaluation:"
    )
    response = llm.invoke(prompt)
    text = response.content.strip()
    verdict = "APPROVED" if text.upper().startswith("APPROVED") else "REJECTED"
    reason = text.split("-", 1)[-1].strip() if "-" in text else text
    return {"lens": lens, "verdict": verdict, "reason": reason}


def ensemble_judge(task: str, output: str) -> str:
    results: list[JudgeResult] = [
        run_judge(lens, instruction, task, output)
        for lens, instruction in LENSES.items()
    ]

    print("\n[Ensemble Judge Results]")
    for r in results:
        print(f"  Lens={r['lens']:<14} | Verdict={r['verdict']:<8} | Reason: {r['reason']}")

    approved_count = sum(1 for r in results if r["verdict"] == "APPROVED")
    threshold = 2
    final = "APPROVED" if approved_count >= threshold else "REJECTED"
    print(f"\n[Majority Vote] {approved_count}/3 approved — Final decision: {final}")
    return final


def main():
    task = "What is the capital of France?"
    output = "The capital of France is Paris, a city known for the Eiffel Tower."

    print(f"[Task]   {task}")
    print(f"[Output] {output}")

    decision = ensemble_judge(task, output)
    print(f"\n[Result] {decision}")


if __name__ == "__main__":
    main()
