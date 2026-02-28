"""
LLM Client Abstraction Layer.

Purpose:
Wrap OpenAI API calls in a single function.

Why:
- Decouples business logic from API implementation.
- Makes it easy to switch providers.
- Enables centralized token tracking and logging.
"""

import os
import time

from openai import OpenAI
from dotenv import load_dotenv
from config import TEMPERATURES, MODEL, MAX_RETRIES
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

def call_llm(prompt):
    """
    Calls the LLM with deterministic settings.

    Args:
        prompt (str): The full prompt to send to the model.

    Returns:
        dict: {
            "text": model output text,
            "usage": token usage metadata
            "latency": token latency metadata
        }
    """
    try:
        start_time = time.time()
        response = client.responses.create(
            model=MODEL,
            input=prompt,
            temperature=TEMPERATURES[0]
        )
        latency = time.time() - start_time
        return {
            "text": response.output_text,
            "usage": response.usage,
            "latency": latency
        }

    except Exception as e:
        print("LLM CALL FAILED:", type(e), str(e))
        raise
