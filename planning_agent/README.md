# Week 5 --- Planning Agent (Multi-Step Reasoning Engine)

## Overview

This project implements a robust multi-step Planning Agent
architecture.\
Unlike simple single-shot LLM prompts, this system decomposes complex
tasks into structured steps and executes them with validation, repair,
retry control, and cost tracking.

This is a production-style reasoning engine built with modular
architecture.

------------------------------------------------------------------------

# Architecture

User Task\
Plan Verification\
Execute\
Repair (if needed)\
Track Cost + Latency\
planner.py \# Task
decomposition + plan verification validator.py \# Step correctness validation llm_agent.py \# LLM
abstraction layer config.py
\# Configuration settings

------------------------------------------------------------------------

# Core Concepts Implemented

## 1. Task Decomposition (Planner)

The planner converts high-level instructions into ordered executable
steps.

Example:

Task: "Generate regression test plan for login API"

Generated Plan: 1. Identify login API endpoints\
2. List input parameters\
3. Generate positive test cases\
4. Generate negative test cases\
5. Define expected outcomes

------------------------------------------------------------------------

## 2. Plan Verification (Pre-Execution Reflection)

Before execution, the plan is verified using the model itself.

Why? Initial plans may be incomplete or logically inconsistent.

The verification step improves plan quality before execution begins.

------------------------------------------------------------------------

## 3. Multi-Step Execution Engine

Each step is executed sequentially.

Execution includes:

-   Context propagation from previous steps
-   Deterministic LLM calls
-   Structured logging
-   Retry control

------------------------------------------------------------------------

## 4. Context Propagation

Each step receives accumulated context from previous steps:

Context so far: - Step 1 output - Step 2 output - Step 3 output

This enables dependent reasoning across steps.

------------------------------------------------------------------------

## 5. Validation Layer

Each step is validated.

Current implementation: - LLM-based validation (YES / NO)

Production upgrade recommendation: - Hybrid validation (rule-based + LLM
fallback)

------------------------------------------------------------------------

## 6. Repair Loop

If validation fails:

-   Reflection prompt is triggered
-   Step output is improved
-   Validation runs again
-   Retry limit enforced

This prevents full workflow restart.

------------------------------------------------------------------------

## 7. Failure Escalation

If a step fails after MAX_RETRIES:

-   Execution stops
-   Exception raised
-   Prevents silent logical corruption

------------------------------------------------------------------------

## 8. Cost & Latency Tracking

Every LLM call tracks:

-   Total tokens used
-   Latency per call
-   Cumulative cost per run

This is critical for production engineering.

Example output:

Total Tokens Used: 5323\
Total Latency: 37 seconds

------------------------------------------------------------------------

This system includes:

-   Planner
-   Plan verification
-   Executor
-   Validator
-   Repair loop
-   Retry logic
-   Context memory
-   Cost tracking
-   Failure escalation

This represents a fully functional multi-step autonomous reasoning
engine.

------------------------------------------------------------------------

# How to Run

1.  Set your OPENAI_API_KEY environment variable
2.  Install dependencies
3.  Run:

python main.py

------------------------------------------------------------------------

"How did you implement your planning agent?"

You can respond:

"I designed a modular Planner--Executor--Validator architecture with
pre-execution plan verification, context propagation across steps,
reflection-based repair loops, retry control, failure escalation, and
token-level cost tracking. The system maintains structured execution
state and supports multi-step autonomous reasoning."

------------------------------------------------------------------------

# Summary

This project demonstrates advanced agent architecture beyond simple
prompt engineering.\
It models structured reasoning, robustness, and production-level
observability.
