import os
from google import genai
from google.genai import types
from tools import TOOL_SCHEMAS
from agent import run_agent

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        tools=[{"function_declarations": TOOL_SCHEMAS}]
    ),
)

print(run_agent(chat, "what's the weather in delhi"))
print(run_agent(chat, "what is the temperature(in Fahrenheit) in delhi?"))
print(run_agent(chat, "what is 15 plus 2 "))