from config import MODE

if MODE == "openai":
    from brain.llm_openai import get_reply
else:
    from brain.llm_local import get_reply

__all__ = ["get_reply"]
