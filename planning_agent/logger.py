"""
Logging Module.

Purpose:
Provide structured logging for each step execution.

Why:
Observability is critical in agent systems.
"""

def log_step(step_result):
    """
    Logs step execution result.

    Args:
        step_result (StepResult): Result of a single step.
    """
    print("\nStep execution result:")
    print(f"Step: {step_result.step}")
    print(f"Success: {step_result.success}")
    print(f"Retries: {step_result.retries}")
    print(f"Output: {step_result.output}")
