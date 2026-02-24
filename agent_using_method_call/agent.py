from tools.calculator import calculator
from tools.web_search import web_search
from tools.file_reader import read_file

TOOLS = {
    "calculator": calculator,
    "search": web_search,
    "file_reader": read_file,
}

AGENT_PROMPT = """
You are a strict tool-using agent.

You MUST follow these rules:

1. If a tool is needed, respond ONLY in this format:

ACTION: tool_name
INPUT: input_value

2. After receiving tool result, you MUST produce:

FINAL: answer

3. DO NOT ask user questions.
4. DO NOT explain yo
5. DO NOT produce conversational text.
6. Always finish with FINAL within 1-2 steps.

Available tools:
- calculator (expression)
- search (query)
- file_reader (path)
"""

from utils.llm_client import generate

def run_agent(user_input):

    conversation = user_input

    for _ in range(5):   # max steps

        prompt = AGENT_PROMPT + "\nUser: " + conversation
        response = generate(prompt, temperature=0)

        # ---- Parse ACTION ----
        if "ACTION:" in response:
            tool_name = response.split("ACTION:")[1].split("\n")[0].strip()
            tool_input = response.split("INPUT:")[1].strip()

            if tool_name in TOOLS:
                result = TOOLS[tool_name](tool_input)
                conversation += f"\nTool Result: {result}"
            else:
                conversation += "\nTool not found"

        elif "FINAL:" in response:
            return response.split("FINAL:")[1].strip()

    return "Failed to complete"
