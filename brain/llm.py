import ollama
from config import LLM_MODEL


def get_reply(messages: list) -> str:
    """
    Sends the conversation history to a local Ollama LLM and returns its reply.
    Make sure Ollama is running: `ollama serve` (it auto-starts on most installs).
    Make sure you've pulled the model: `ollama pull llama3.2`
    """
    response = ollama.chat(
        model=LLM_MODEL,
        messages=messages,
        options={
            "temperature": 0.7,
            "num_predict": 300,   # Max tokens in reply (keep short for voice)
        }
    )
    return response["message"]["content"].strip()
