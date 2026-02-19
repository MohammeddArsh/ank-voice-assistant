from config import SYSTEM_PROMPT


class ConversationMemory:
    """
    Maintains the full conversation history for multi-turn context.
    OpenAI's API is stateless, so we send the whole history each time.
    """

    def __init__(self):
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def add_user_message(self, text: str):
        self.messages.append({"role": "user", "content": text})

    def add_assistant_message(self, text: str):
        self.messages.append({"role": "assistant", "content": text})

    def get_messages(self) -> list:
        return self.messages

    def trim_if_needed(self, max_turns: int = 20):
        """
        Keep the system prompt + last N turns to avoid hitting token limits.
        Each turn = 1 user message + 1 assistant message = 2 entries.
        """
        system = self.messages[:1]
        conversation = self.messages[1:]
        if len(conversation) > max_turns * 2:
            conversation = conversation[-(max_turns * 2):]
        self.messages = system + conversation
