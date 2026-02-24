from utils.llm_client import generate


TEST_DATA = [
    ("I absolutely love this phone", "positive"),
    ("This is terrible and disappointing", "negative"),
    ("The movie was average", "neutral"),
    ("Amazing experience, very happy", "positive"),
    ("Worst purchase ever", "negative"),
]


ZERO_SHOT_PROMPT = """
Classify the sentiment of this text as one of:
positive, negative, neutral.

Text: {text}
Answer with only one word.
"""


FEW_SHOT_PROMPT = """
Classify the sentiment of this text as one of:
positive, negative, neutral.

Examples:
Text: I love this product, it is amazing
Sentiment: positive

Text: This is the worst service I have ever used
Sentiment: negative

Text: The product is okay, nothing special
Sentiment: neutral

Now classify:

Text: {text}
Answer with only one word.
"""


def run_exp():
    print("=== Experiment 4: Few-shot vs Zero-shot ===\n")

    zero_correct = 0
    few_correct = 0

    for text, true_label in TEST_DATA:

        # ---- Zero-shot ----
        resp_zero = generate(ZERO_SHOT_PROMPT.format(text=text), temperature=0)
        pred_zero = resp_zero.strip()

        # ---- Few-shot ----
        resp_few = generate(FEW_SHOT_PROMPT.format(text=text), temperature=0)
        pred_few = resp_few.strip()

        print(f"Text: {text}")
        print(f"True: {true_label}")
        print(f"Zero-shot: {pred_zero}")
        print(f"Few-shot : {pred_few}")
        print("----")

        if pred_zero == true_label:
            zero_correct += 1
        if pred_few == true_label:
            few_correct += 1

    print("\nZero-shot Accuracy:", zero_correct / len(TEST_DATA))
    print("Few-shot Accuracy :", few_correct / len(TEST_DATA))
