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

- tools.py - tool functions + the @tool decorator that auto-registers them
- agent.py - the generic tool-calling loop
- main.py - binds everything together (entry point)
- memory.py - serialize/deserialize conversation history to/from JSON, for persistence
- rag.py - embeddings, cosine similarity, and retrieval over a small knowledge base
- evals.py - automated test suite checking tool-selection correctness


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

## Persistent Memory across Sessions

The agent doesn't forget when the program exits. Conversation history includes
every tool call and result which is saved to `history.json` after each run, and loaded 
back in on the next run, so the agent has real context from previous sessions, not 
just within a single run.

```python
if os.path.exists("history.json"):
    initial_history = load_history("history.json")
else:
    initial_history = []

chat = client.chats.create(model=..., history=initial_history, ...)
```

Confirmed working: after saving a session where the agent looked up Delhi's weather, 
a fresh run correctly answered a follow-up question about that weather *without* 
re-calling the tool which is the proof that the loaded history is actually being used by the model, 
not just sitting there unused.

## Retrieval-augmented answers (RAG)

The agent can answer questions using a small personal knowledge base, not just its 
training data or tool calls to external APIs. Built from scratch that means no vector DB library, 
no LangChain retriever:

- Each knowledge entry gets embedded via Gemini's `embed_content` API
- A hand-written cosine similarity function ranks stored entries against a query's 
  embedding
- The best-matching entry is returned as a tool result, same pattern as any other tool

## Eval suite

Confidence that the agent picks the right tool isn't just assumed but tested too. 
`evals.py` runs a set of test cases against fresh chat sessions (no shared 
history between tests, so results are reproducible regardless of prior conversations) 
and checks whether the expected tools were actually called.

Two levels of checking:
- **Membership** : for single-tool queries, was the expected tool called at all
- **Sequence** : for multi-step queries (e.g. "temperature in Fahrenheit" requires 
  `get_weather` then `cel_to_far`, in that order), a subsequence check confirms the 
  right tools ran in the right relative order, while still tolerating extra retries 
  the model sometimes makes on its own (observed happening naturally with 
  `search_knowledge`)

```python
def is_subsequence(expected, actual):
    expected_index = 0
    for tool in actual:
        if expected_index < len(expected) and tool == expected[expected_index]:
            expected_index += 1
    return expected_index == len(expected)
```

Run it:
```bash
python evals.py
```

## Current limitations

- Knowledge base is a small, hardcoded list, no ingestion pipeline for real 
  documents yet
- Conversation history in `history.json` grows unbounded across sessions
- Eval coverage checks tool selection, not answer content/quality

## What's next

- Broader eval coverage (answer correctness, not just which tool got called)
- Truncation for growing conversation history
- A real vector store, if the knowledge base grows past a handful of entries