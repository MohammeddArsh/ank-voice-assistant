from openai import OpenAI
from config import OPENAI_API_KEY, LLM_MODEL_OPENAI

client = OpenAI(api_key=OPENAI_API_KEY)

def get_reply(messages: list) -> str:
    response = client.chat.completions.create(
        model=LLM_MODEL_OPENAI,
        messages=messages,
        temperature=0.7,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()
