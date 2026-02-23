import json
from config import PROMPT, RUNS_PER_TEMP, TEMPERATURES
from utils.llm_client import generate
import os

def run_exp():
    for temperature in TEMPERATURES:
        result = []
        print("Running temperature {}".format(temperature))
        for i in range(RUNS_PER_TEMP):
            output = generate(PROMPT, temperature)
            print(f"Run {i+1}, Result: {output}")
            result.append(output)

        os.makedirs("results", exist_ok=True)
        with open(f"results/temp_{temperature}_runs.txt", "w") as f:
            json.dump(result, f, indent=4)

if __name__ == "__main__":
    run_exp()