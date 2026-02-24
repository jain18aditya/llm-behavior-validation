TOOLS_SCHEMA = [
    {
        "type": "function",
        "name": "email_summarizer",
        "description": "Summarizes an email and detects if action is required",
        "parameters": {
            "type": "object",
            "properties": {
                "email_text": {"type": "string"}
            },
            "required": ["email_text"]
        }
    },
    {
        "type": "function",
        "name": "json_extractor",
        "description": "Use this tool ONLY when extracting structured order details (Order ID, Amount, Status) from full text. Always pass the ENTIRE user text.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string"}
            },
            "required": ["text"]
        }
    },
    {
        "type": "function",
        "name": "task_planner",
        "description": "Creates a structured task plan",
        "parameters": {
            "type": "object",
            "properties": {
                "goal": {"type": "string"}
            },
            "required": ["goal"]
        }
    }
]