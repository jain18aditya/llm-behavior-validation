"""
Validator Module.

Purpose:
Verify whether step output correctly completes the intended task.

Why:
Enables reflection loop and reliability.
Prevents silent logical errors.
"""

from llm_agent import call_llm

def validate_step(step: str, output:str):
    """
    Validates whether a step output is correct.

    Args:
        step (str): Original step instruction.
        output (str): Generated output.

    Returns:
        bool: True if valid, False otherwise.
    """
    prompt = f"""
    Step:
    {step}

    Output:
    {output}

    Did the output correctly complete the step?
    Answer ONLY: YES or NO.
    """
    response = call_llm(prompt)
    return "YES" in response["text"].upper()