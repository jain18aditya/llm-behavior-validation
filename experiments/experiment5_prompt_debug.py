from utils.llm_client import generate


BAD_PROMPT = """
Summarize this:
Python is a programming language used in many fields like AI, web, automation, and data science.
"""


GOOD_PROMPT = """
You are a concise technical writer.

Summarize the following text in exactly ONE sentence (max 20 words).

Return ONLY plain text. No explanation.

Text:
Python is a programming language used in many fields like AI, web, automation, and data science.
"""


def run_exp():
    print("=== Experiment 5: Prompt Debugging ===\n")

    # ---- Bad Prompt ----
    bad_output = generate(BAD_PROMPT, temperature=0)
    print("Ambiguous Prompt Output:\n")
    print(bad_output)
    print("\n----------------------------\n")

    # ---- Improved Prompt ----
    good_output = generate(GOOD_PROMPT, temperature=0)
    print("Improved Prompt Output:\n")
    print(good_output)

    # Save results
    with open("results/exp5_prompt_debugging.txt", "w") as f:
        f.write("BAD PROMPT OUTPUT:\n")
        f.write(str(bad_output) + "\n\n")
        f.write("GOOD PROMPT OUTPUT:\n")
        f.write(str(good_output) + "\n")

    print("\nResults saved → results/exp5_prompt_debugging.txt")