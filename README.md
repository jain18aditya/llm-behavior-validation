# LLM Behavior & Agent Engineering Roadmap

This repository documents a structured, hands-on learning journey into **LLM behavior, prompt engineering, and agentic workflow design**, progressing from foundational model experiments to a deterministic function-calling assistant with guardrails and retry logic.

The goal of this project is to deeply understand:

- How LLMs work internally
- How prompting affects behavior
- How to build agents from scratch
- How to design guardrails and reliability
- How to control cost and determinism

This is framework-independent agent engineering.

---

# 📁 Project Structure

```
project-root/
│
├── .env
├── week1/
│   ├── temperature_experiment.py
│   ├── token_experiment.py
│   ├── json_experiment.py
│   ├── fewshot_experiment.py
│   └── prompt_debugging.py
│
├── week2/
│   ├── main.py
│   ├── agent.py
│   └── tools/
│
├── week3/
│   ├── main.py
│   ├── assistant.py
│   ├── schemas.py
│   └── tools/
│
└── README_FULL_AGENTIC_ROADMAP.md
```

---

# ⚙️ Environment Setup

## 1️⃣ Create Virtual Environment

### Mac/Linux
```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows
```bash
python -m venv .venv
.venv\Scripts#ctivate
```

---

## 2️⃣ Install Dependencies

```bash
pip install openai python-dotenv
```

(Optional: use `requirements.txt` if available.)

---

# 🔐 .env Configuration (Required)

Create a `.env` file at the **root of the project**.

```text
project-root/
├── .env   ← MUST be here
```

### Sample `.env`

```text
OPENAI_API_KEY=your_api_key_here
MODEL=gpt-4.1-mini
```

⚠️ Important:
- Do NOT commit your real API key
- Add `.env` to `.gitignore`
- API keys must remain local

---

# 🧠 Week 1 — LLM + OpenAI API Foundation

## Concepts Learned

### 1️⃣ Tokens
- LLM reads tokens, not words
- Cost depends on tokens
- Context depends on tokens
- Long prompts increase cost and latency

### 2️⃣ Context Window
- Max tokens model can process in one request
- Prompt + response must fit in window
- Long conversations cause truncation
- Leads to need for RAG

### 3️⃣ Temperature
- Controls randomness
- 0 → deterministic
- 0.7 → balanced
- 1 → creative / unstable

### 4️⃣ Top-p
- Controls probability sampling range
- Typically left default

### 5️⃣ Max Tokens
- Limits output length
- Controls cost

### 6️⃣ System vs User Messages
- System → behavior control
- User → task input

### 7️⃣ Cost Concept
- Cost = input tokens + output tokens
- Prompt design directly affects cost

---

## 🧪 Experiments Conducted

### Experiment 1 — Temperature Impact
Prompt: “Explain Python in 2 lines”
- Run with temperature = 0
- Run with temperature = 1
Observed:
- Determinism vs creativity
- Repetition vs variation

---

### Experiment 2 — Token Size Impact
- Short prompt
- Long prompt
Observed:
- Response quality
- Latency difference
- Token usage difference

---

### Experiment 3 — Force JSON Output
Prompt: “Return ONLY valid JSON: {"summary": string}”
Tested:
- With structure instruction
- Without structure instruction
Observed:
- Hallucination
- Format reliability

---

### Experiment 4 — Few-shot vs Zero-shot
Task: Sentiment classification
- Without examples
- With 3 examples
Observed:
- Accuracy differences
- Output structure variation

---

### Experiment 5 — Prompt Debugging
- Gave ambiguous prompt
- Improved with:
  - Role
  - Constraints
  - Structure
Observed improvement.

---

## 🎯 Week 1 Deliverable

CLI Smart Chatbot:
- Structured output
- Logging
- Retry handling

---

# 🤖 Week 2 — ReAct Agent (Reason → Act → Observe)

## Concepts Learned

- Agent loop
- Tool usage
- Execution cycles
- Failure modes
- Why string parsing is fragile

---

## Tools Built

- Calculator
- Web Search (mocked)
- File Reader

---

## Architecture

User  
↓  
Agent  
↓  
Reason  
↓  
Select Tool  
↓  
Execute Tool  
↓  
Observe  
↓  
Respond  

---

## Key Learnings

- String-based action parsing is unstable
- Infinite loops possible
- No schema validation
- No deterministic guardrails
- Need structured tool calling

---

## Week 2 Deliverable

Tool-Using Agent:
- User asks question
- Agent selects tool
- Tool executes
- Agent responds

---

# 🛠 Week 3 — Function Calling + Structured Tools

## Concepts Learned

- Function calling
- JSON Schema
- Guardrails
- Deterministic execution
- Retry logic
- Tool whitelist enforcement
- Parallel tool control

---

## Tools Built

- Email Summarizer
- JSON Extractor
- Task Planner

---

## Architecture

User  
↓  
LLM (Function Calling)  
↓  
Schema Validation  
↓  
Execution Layer  
↓  
Guardrails  
↓  
Structured Response  

---

## Guardrails Implemented

- Single tool call enforcement
- Disabled parallel tool calls
- Tool whitelist validation
- JSON argument validation
- Retry on malformed model output
- Structured response format
- Deterministic behavior (temperature=0)
- Token usage tracking
- Error handling

---

## Example Output

```json
{
  "status": "success",
  "tool": "json_extractor",
  "data": {
    "order_id": "123",
    "amount": "50",
    "status": "Shipped"
  }
}
```

---

## Week 3 Deliverable

Personal Assistant Agent (v1)

---


Questions:

- What is a token?
- Why token size affects cost?
- Temperature vs top-p?
- What is context window?
- Why model forgets long conversations?
- How to reduce hallucination?
- How to force JSON output?
- What happens internally when calling LLM API?
- What is few-shot prompting?

---

# 📚 Important Learning Resources

Core LLM + OpenAI
- OpenAI Quickstart  
- Responses API  
- Function Calling  
- Embeddings  
- Evals  

Prompt Engineering
- DeepLearning.AI Prompt Engineering Course  

Agents + RAG
- LangChain Docs  
- LangGraph Tutorials  
- RAG Guide  

Multi-Agent Systems
- CrewAI Docs  
- Microsoft AutoGen  

Vector Databases
- FAISS  

Backend + Automation
- FastAPI  
- Playwright Python  

Observability
- LangSmith  

---

# 🔒 Security Notice

- No API keys stored in repository
- `.env` required locally
- Secrets excluded from version control
- Personal API key not checked in

---
