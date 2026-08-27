# Tool-Calling LLM Agent (from scratch)

- AI agent built from scratch in Python using the Gemini API 
- no LangChain or other agent frameworks. 
- Built to genuinely understand how tool-calling agents work under the hood, not just use a pre-built one.

## What it does

- Runs a tool-calling loop: the model decides which tool to call, the code executes it, 
  the result goes back to the model, repeat until the model has enough info to answer.
- Supports chaining multiple tool calls in sequence (e.g. fetch weather -> convert units) 
  without any hardcoded logic connecting them, the model decides the sequence itself.
- Reuses conversation history intelligently and it won't re-fetch data it already has from 
  earlier in the same session.

## The interesting part: self-registering tools

Adding a new tool is just:

```python
@tool(description="add two numbers")
def add_numbers(a: float, b: float) -> float:
    return a + b
```

The `@tool` decorator reads the function's type hints (`__annotations__`) and 
automatically generates the JSON schema Gemini needs to know the tool exists, no 
separate hand-written schema dict required. It also registers the function itself, so 
there's a single source of truth per tool instead of keeping a function, a schema, and a 
registry entry in sync by hand.

## Project structure

- tools.py — tool functions + the @tool decorator that auto-registers them
- agent.py — the generic tool-calling loop
- main.py — binds everything together (entry point)


## Setup

```bash
git clone <this repo>
cd agent-framework
python -m venv venv
venv\Scripts\activate.bat  # Windows PowerShell & see docs for other shells
pip install google-genai
```

Get a free API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey), 
then set it as an environment variable :

```bash
$env:GEMINI_API_KEY="your_key_here" # inside PowerShell
```

Run it:
```bash
python main.py
```

## What's next

- Memory across sessions (currently only remembers within a single run)
- A RAG tool for retrieval-augmented answers
- More robust error handling around tool execution