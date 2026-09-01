

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

