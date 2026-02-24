import json
from utils.llm_client import generate, generate_full_response

PROMPT_NO_STRUCTURE = """
Summarize Python in 2 lines and return JSON.
"""

PROMPT_WITH_STRUCTURE = """
Return ONLY valid JSON in this exact format:
{
  "summary": string
}

Do not include explanations.
Do not include markdown.
Do not include text outside JSON.

Summarize Python in 2 lines.
"""


def validate_json(output):
    try:
        parsed = json.loads(output)
        print("✅ Valid JSON")
        return True
    except Exception as e:
        print("❌ Invalid JSON:", str(e))
        return False


def run_exp():
    print("=== Experiment 3: Force JSON Output ===\n")

    # ---- Without Structure ----
    print("---- Without Structure Instruction ----")
    resp1 = generate_full_response(PROMPT_NO_STRUCTURE, temperature=0)
    output1 = resp1.output_text
    print("Output:\n", output1)
    validate_json(output1)

    print("Tokens:", resp1.usage.total_tokens, "\n")

    # ---- With Structure ----
    print("---- With Structure Instruction ----")
    resp2 = generate_full_response(PROMPT_WITH_STRUCTURE, temperature=0)
    output2 = resp2.output_text
    print("Output:\n", output2)
    validate_json(output2)

    print("Tokens:", resp2.usage.total_tokens)

    # Save results
    with open("results/exp3_json_output.txt", "w") as f:
        f.write("WITHOUT STRUCTURE:\n")
        f.write(output1 + "\n\n")
        f.write("WITH STRUCTURE:\n")
        f.write(output2 + "\n")