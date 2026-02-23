import time
from utils.llm_client import generate, generate_full_response


SHORT_PROMPT = "Explain Python in 2 lines"

LONG_PROMPT = """
Python is a widely used high-level programming language known for readability,
simplicity, and strong ecosystem. It supports multiple paradigms including
object-oriented, functional, and procedural programming. Python is used in
automation, data science, machine learning, web development, DevOps, scripting,
and AI systems. Explain Python in 2 lines.
"""


def run_exp():
    print("=== Experiment 2: Token Size Impact ===\n")

    # ---- Long Prompt ----
    start = time.time()
    long_output = generate_full_response(LONG_PROMPT, temperature=0)
    long_latency = time.time() - start

    print("LONG PROMPT OUTPUT:\n", long_output)
    print("Latency:", round(long_latency, 3), "seconds\n")

    # ---- Short Prompt ----
    start = time.time()
    short_output = generate_full_response(SHORT_PROMPT, temperature=0)
    short_latency = time.time() - start

    print("SHORT PROMPT OUTPUT:\n", short_output)
    print("Latency:", round(short_latency, 3), "seconds\n")

    # Save results
    with open("results/exp2_token_impact.txt", "w") as f:
        f.write("SHORT PROMPT OUTPUT:\n" + short_output.output_text.strip() + "\n\n")
        f.write("SHORT LATENCY: " + str(short_latency) + "\n\n")
        f.write("LONG PROMPT OUTPUT:\n" + long_output.output_text.strip() + "\n\n")
        f.write("LONG LATENCY: " + str(long_latency) + "\n")

    print("Input tokens :", long_output.usage.input_tokens)
    print("Output tokens:", long_output.usage.output_tokens)
    print("Total tokens :", long_output.usage.total_tokens)

    print("Input tokens :", short_output.usage.input_tokens)
    print("Output tokens:", short_output.usage.output_tokens)
    print("Total tokens :", short_output.usage.total_tokens)

    print("Results saved → results/exp2_token_impact.txt")