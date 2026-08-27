from google.genai import types
from tools import TOOL_IMPLS

def run_agent(chat, user_message: str):
    response = chat.send_message(user_message)

    while True:
        parts = response.candidates[0].content.parts

        # find a function_call part, if any
        function_call_part = None
        for part in parts:
            if part.function_call is not None:
                function_call_part = part
                break

        if function_call_part is None:
            # no tool call -> model gave a final text answer -> done
            return response.text

        fc = function_call_part.function_call
        print(f"[agent] calling tool: {fc.name}({fc.args})")

        tool_fn = TOOL_IMPLS[fc.name]
        result = tool_fn(**fc.args)   # unpack args dict directly as kwargs

        # sending result back into the same chat, then loop again
        response = chat.send_message(
            types.Part(
                function_response=types.FunctionResponse(
                    name=fc.name,
                    response={"result": result},
                    id=fc.id,
                )
            )
        )