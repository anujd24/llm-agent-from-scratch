import os
from google import genai
from google.genai import types
from agent import run_agent
import time
from tools import TOOL_SCHEMAS

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def is_subsequence(expected, actual):
    expected_index = 0  # how many of "expected" we've matched so far

    for tool in actual:
        if expected_index < len(expected) and tool == expected[expected_index]:
            expected_index += 1  # found the next expected tool, in order — advance

    return expected_index == len(expected)  # did we find all of them?

test_case = [
    {"query": "what's the weather in Mumbai?", "expected_sequence": ["get_weather"]},
    {"query": "convert 100 celsius to fahrenheit", "expected_sequence": ["cel_to_far"]},
    {"query": "what's 7 plus 12?", "expected_sequence": ["add_numbers"]},
    {"query": "what technologies does Anuj use at work?", "expected_sequence": ["search_knowledge"]},
    {"query": "what is the temperature in farhenheit in Delhi?", "expected_sequence" : ["get_weather", "cel_to_far"]}
]

def run_evals(test_case):
    passed = 0
    failed = 0

    for case in test_case:
        time.sleep(15)
        chat = client.chats.create(
            model= "gemini-3.6-flash",
            config = types.GenerateContentConfig(tools=[{"function_declarations": TOOL_SCHEMAS}])
        )
        answer, tools_called = run_agent(chat, case["query"])

        if is_subsequence(case["expected_sequence"], tools_called):
            print(f" pass: '{case['query']}' -> called {tools_called}")
            passed += 1
        else:
            print(f" fail: '{case['query']}' -> expected {case['expected_sequence']}, got {tools_called}")
            failed +=1

    print(f"\n{passed}/{passed + failed} passed")

run_evals(test_case)