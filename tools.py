from rag import retrieve, store


PY_TYPE_TO_JSON = {
    str : "string",
    float : "number",
    int : "integer",
    bool : "boolean"
}

TOOL_IMPLS= {}
TOOL_SCHEMAS = []

def tool(description) : 
    def decorator(fn) :
        properties = {};
        required = [];
        for(name, __type) in fn.__annotations__.items():
            if name == "return" :
                continue
            # print(name, __type)
            properties[name] = {"type" : PY_TYPE_TO_JSON[__type]}
            required.append(name);

        schema = {
            "name" : fn.__name__,
            "description" : description,
            "parameters" : {
                "type" : "object",
                "properties" : properties,
                "required" : required
            },
        }

        TOOL_SCHEMAS.append(schema)
  
        TOOL_IMPLS[fn.__name__] = fn
        return fn
    return decorator

@tool(description="get current weather of a city")
def get_weather(city:str) -> str:
    return f"it's sunny in {city}, 28 degree celsius"

@tool(description="convert degree to farhenheit")
def cel_to_far(celsius : float) -> float:
    return celsius * 1.8 + 32 

@tool(description="add two numbers")
def add_numbers(a:float, b:float) -> float:
    return a + b

@tool(description="search Anuj's personal knowledge base for relevant information")
def search_knowledge(query : str) -> str:
    text, score = retrieve(query, store)
    return text

# print(get_weather.__annotations__)