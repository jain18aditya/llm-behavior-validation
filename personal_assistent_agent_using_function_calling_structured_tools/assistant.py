import json
from tools.json_extractor import json_extractor
from tools.task_planner import task_planner
from tools.email_summarizer import email_summarizer
from schemas import TOOLS_SCHEMA
from utils.llm_client import get_client, get_model
from config import MAX_RETRIES

client = get_client()

TOOLS_MAP = {
    "email_summarizer": email_summarizer,
    "task_planner": task_planner,
    "json_extractor": json_extractor
}

def run_assistant(user_input):

    for attempt in range(MAX_RETRIES):

        response = client.responses.create(
            model=get_model(),
            input=[
                {
                    "role": "system",
                    "content": "You are a structured assistant. Always call exactly one appropriate tool. Never call multiple tools."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
            temperature=0,
            parallel_tool_calls=False
        )

        if not response.output:
            if attempt == MAX_RETRIES - 1:
                return {"status": "error", "message": "Empty model response"}
            continue

        # --- Find function call ---
        tool_call = None
        for item in response.output:
            if item.type == "function_call":
                tool_call = item
                break

        if not tool_call:
            return {"status": "text", "output": response.output_text}

        tool_name = tool_call.name

        if tool_name not in TOOLS_MAP:
            return {"status": "error", "message": f"Unknown tool: {tool_name}"}

        # --- Parse arguments (retry if JSON invalid) ---
        try:
            arguments = json.loads(tool_call.arguments)
        except json.JSONDecodeError:
            print(f"Retry {attempt+1}: Invalid JSON from model")
            if attempt == MAX_RETRIES - 1:
                return {"status": "error", "message": "Invalid JSON arguments"}
            continue

        # --- Execute tool ---
        try:
            result = TOOLS_MAP[tool_name](**arguments)
        except TypeError as e:
            return {"status": "error", "message": f"Tool argument mismatch: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": f"Tool execution failed: {str(e)}"}

        # --- Token usage ---
        usage = response.usage
        print("TOKENS:",
              "input:", usage.input_tokens,
              "output:", usage.output_tokens,
              "total:", usage.total_tokens)

        return {
            "status": "success",
            "tool": tool_name,
            "data": result
        }