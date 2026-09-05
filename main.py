import os
from google import genai
from google.genai import types
from tools import TOOL_SCHEMAS
from agent import run_agent
from memory import save_history
from memory import load_history

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

if os.path.exists("history.json"):
    initial_history = load_history("history.json")
else :
    initial_history = []

chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        tools=[{"function_declarations": TOOL_SCHEMAS}]
    ),
    history = initial_history
)


print(run_agent(chat, "what was the weather I asked about earlier?"))
print(run_agent(chat, "what technologies were used at my workplace ?"))


# history = chat.get_history()
# print(json.dumps(serialize_history(history)))
# print(type(history))

# if history:
#     print(type(history[0]))

save_history(chat.get_history())
