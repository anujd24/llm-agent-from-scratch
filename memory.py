from google.genai import types
import json

def serialize_history(history):
    serialized = []

    for item in history:
        entry = {"role" : item.role, "parts" : []}

        for part in item.parts:
            if part.text is not None:
                data = {"type": "text", "text": part.text}
                entry["parts"].append(data)

            elif part.function_call is not None:
                data = {"type" : "function_call", "name": part.function_call.name, "args" : part.function_call.args, "id": part.function_call.id}
                entry["parts"].append(data)

            elif part.function_response is not None:
                data = {"type" : "function_response", "name" : part.function_response.name, "id" : part.function_response.id, "response" : part.function_response.response}
                entry["parts"].append(data)

        serialized.append(entry)
    return serialized

def deserialize_history(serialized):
    history = []
    for entry in serialized:
        parts =[]
        for part_data in entry["parts"]:
            if part_data["type"] == "text":
                parts.append(types.Part.from_text(text=part_data["text"]))
            elif part_data["type"] == "function_call":
                parts.append(types.Part.from_function_call(name=part_data["name"], args=part_data["args"]))
            elif part_data["type"] == "function_response":
                parts.append(types.Part.from_function_response(name=part_data["name"], response=part_data["response"]))

        history.append(types.Content(role=entry["role"], parts=parts))
    return history

def save_history(history, filepath="history.json"):
    with open(filepath, "w") as f:
        json.dump(serialize_history(history), f, indent=2)

def load_history(filepath="history.json"):
    with open(filepath, "r") as f:
        return deserialize_history(json.load(f));