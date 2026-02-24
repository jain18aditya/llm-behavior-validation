from openai import OpenAI
import os
import json
from tools.json_extractor import json_extractor
from tools.task_planner import task_planner
from tools.email_summarizer import email_summarizer
from schemas import TOOLS_SCHEMA
from utils.llm_client import get_client, get_model

client = get_client()

TOOLS_MAP = {
    "email_summarizer": email_summarizer,
    "task_planner": task_planner,
    "json_extractor": json_extractor
}

def run_assistant(user_input):
    response = client.responses.create(model=get_model(),
                                       input=user_input,
                                       tools=TOOLS_SCHEMA,
                                       tool_choice="auto",
                                       temperature=0,
                                       parallel_tool_calls=False)

    for item in response.output:
        if item.type == "function_call":
            tool_name = item.name
            argument = json.loads(item.arguments)

            if tool_name in TOOLS_MAP:
                result = TOOLS_MAP[tool_name](**argument)

                return {
                    "tool_used": tool_name,
                    "result": result
                }
    return response.output_text

