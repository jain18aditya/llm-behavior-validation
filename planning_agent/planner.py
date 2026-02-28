"""
Planner Module.

Purpose:
Convert high-level user task into structured executable steps.

Why:
Separates reasoning (planning) from execution logic.
Enables plan verification and refinement independently.
"""
import json
from llm_agent import call_llm
from models import Plan

def create_plan(task: str):
    """
    Generates an ordered execution plan for a complex task.

    Args:
        task (str): High-level user instruction.

    Returns:
        Plan: Structured plan with ordered steps.
    """
    prompt = f"""
    Break the following task into ordered executable steps.
    Return ONLY valid JSON in this format:
    {{"steps": ["step1", "step2"]}}

    Task:
    {task}
    """
    response = call_llm(prompt)
    data = json.loads(response["text"])
    plan = Plan(**data)
    return plan

def verify_plan(task: str, plan: Plan):
    prompt = f"""
    Task:
    {task}

    Proposed Plan:
    {plan.steps}

    Is this plan sufficient and logically complete?
    If not, return improved plan in JSON format:
    {{"steps": ["..."]}}
    If yes, return the same plan.
    """

    response = call_llm(prompt)
    try:
        improved_plan = json.loads(response["text"])
        return Plan(**improved_plan)
    except json.decoder.JSONDecodeError:
        return Plan

