import json
from collections import Counter
import os

def analyze(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)

    print("/n unique output:", len(set(data)))

    counter = Counter(data)
    print("Most common response")
    print(counter.most_common(1))

    print("All outputs")
    for d in data:
        print(d)


if __name__ == "__main__":
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print("Temp 0 Analysis")
    analyze(f"{PROJECT_ROOT}\\results\\temp_0_runs.txt")

    print("\nTemp 1 Analysis")
    analyze(f"{PROJECT_ROOT}\\results\\temp_1_runs.txt")