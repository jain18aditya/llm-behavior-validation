"""
Main Entry Point.

Purpose:
Orchestrates planning agent workflow.

Why:
Keeps execution centralized and clean.
"""

from planner import create_plan, verify_plan
from executor import execute_plan
from logger import log_step

def run_agent(task: str):
    """
    Runs full planning agent workflow.

    Args:
        task (str): High-level user instruction.
    """
    print("\nCreating Plan...")
    plan = create_plan(task)
    plan = verify_plan(task, plan)

    print("\nExecuting Plan...")
    steps = execute_plan(plan)
    for step in steps:
        log_step(step)
    return steps

if __name__ == "__main__":
    result = []
    task = "Generate regression test plan for login API"
    run_agent(task)
