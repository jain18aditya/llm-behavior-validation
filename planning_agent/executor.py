"""
Executor Module.

Purpose:
Execute structured plan step-by-step with validation and repair loop.

Why:
Implements core autonomous reasoning cycle.
"""
from models import StepResult
from validator import validate_step
from repair import repair_step
from llm_agent import call_llm
from config import MAX_RETRIES

def execute_plan(plan):
    """
    Executes each step in a structured plan.

    Args:
        plan (Plan): Structured plan object.

    Returns:
        List[StepResult]: Results for each executed step.
    """
    result = []
    context = ""
    total_tokens = 0
    total_latency = 0
    for step in plan.steps:
        retries = 0

        # First execution
        response = call_llm(f"Execute step {step}")
        total_tokens += response["usage"].total_tokens
        total_latency += response["latency"]
        output = response["text"]

        success = validate_step(step, output)

        # Repair loop only if needed
        while not success and retries < MAX_RETRIES:
            prompt = f"""
            You are executing a multi-step plan.

            Here is all previous completed work:

            {context}

            Now complete the following step using the previous work if needed.

            Step:
            {step}

            Return only the output for this step.
            """
            response = call_llm(prompt)
            total_tokens += response["usage"]["total_tokens"]
            total_latency += response["latency"]
            output = response["text"]
            success = validate_step(step, output)
            if not success:
                repair_response = repair_step(step, output)
                print(type(repair_response))
                print(repair_response)
                output = repair_response["text"]
                total_tokens += repair_response["usage"]["total_tokens"]
                total_latency += repair_response["latency"]
                retries += 1
        # Update context for next step
        context += f"\nStep: {step}\nOutput: {output}\n"

        result.append(
            StepResult(
                step=step,
                output=output,
                success=success,
                retries=retries
            )
        )

        # Escalation if step fails permanently
        if not success:
            raise Exception(f"Step failed permanently: {step}")

    print("Total Tokens Used:", total_tokens)
    print("Total Latency:", total_latency)
    return result