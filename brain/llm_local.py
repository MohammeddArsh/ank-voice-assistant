import ollama
from config import LLM_MODEL_LOCAL

def get_reply(messages: list) -> str:
    response = ollama.chat(
        model=LLM_MODEL_LOCAL,
        messages=messages,
        options={"temperature": 0.7, "num_predict": 300}
    )
    return response["message"]["content"].strip()
