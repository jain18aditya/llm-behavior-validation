"""
Repair Module.

Purpose:
Improve failed step outputs through reflection.

Why:
Prevents full workflow restart.
Supports partial recovery.
"""

from llm_agent import call_llm

def repair_step(step:str, previous_output:str):
    """
    Attempts to regenerate improved output for failed step.

    Args:
        step (str): Original step instruction.
        previous_output (str): Failed output.

    Returns:
        str: Improved output.
    """
    prompt = f"""
    The following step failed validation.

    Step:
    {step}

    Previous Output:
    {previous_output}

    Improve and regenerate correct output.
    """
    return call_llm(prompt)

