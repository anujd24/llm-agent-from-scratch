import os
from google import genai
import math

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def cosine_similarity(v1, v2):
    dot = 0
    m1 = 0
    m2 = 0
    result = 0
    for i in range(len(v1)):
        dot += v1[i] * v2[i]

        m1 += v1[i]**2

        m2 += v2[i]**2

    finalm1 = math.sqrt(m1)
    finalm2 = math.sqrt(m2)

    result = dot / (finalm1 * finalm2)

    return result


knowledge = [
    "The agent framework was built using the Gemini API with function calling.",
    "The matching engine project will handle order book operations with a lock-free design.",
    "Anuj's EMI is 18000 rupees per month.",
    "The office project uses libuv, hiredis, and SQLite3 for a C-based event-driven server.",
    "GATE 2027 preparation covers both CS and DA papers.",
]

def storage(knowledge):
    store = []

    for text in knowledge:
        result = client.models.embed_content(
            model = "gemini-embedding-001",
            contents=text
        )
        final = result.embeddings[0].values
        store.append({"text" : text, "vector" : final})
    return store

# store = storage(knowledge)
# print(store[0]["text"])
# print(len(store[0]["vector"]))
# print(len(store))

def retrieve(query, store):
    query_result = client.models.embed_content(
        model = "gemini-embedding-001",
        contents = query
    )

    query_vector = query_result.embeddings[0].values

    best_score = -1
    best_entry = None

    for entry in store:
        score = cosine_similarity(query_vector, entry["vector"])

        if score > best_score:
            best_score = score
            best_entry = entry

    return best_entry["text"], best_score

# text, score = retreive("what does Anuj pay for his loan every month?", store)
# print(text, score)

store = storage(knowledge)