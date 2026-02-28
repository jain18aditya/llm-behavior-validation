"""
Data Models for Planning Agent.

Purpose:
Define structured data contracts between modules.

Why:
- Prevent schema ambiguity
- Improve reliability
- Enable validation
- Make debugging easier
"""

from pydantic import BaseModel
from typing import List

class Plan(BaseModel):
    """
    Represents a structured execution plan.

    Attributes:
        steps (List[str]): Ordered list of executable steps.
    """
    steps: List[str]

class StepResult(BaseModel):
    """
    Represents the result of a single step execution.

    Attributes:
        step (str): The step description.
        output (str): Model-generated result.
        success (bool): Whether validation passed.
        retries (int): Number of retry attempts.
    """
    step: str
    output: str
    success: bool
    retries: int