import logging
from models import ChatMessage

logger = logging.getLogger(__name__)

class ChatHistoryManager:
    """
    Simple class to hold ChatMessage types over the lifetime of the conversation.
    Using a class allows you to expand later (like saving history to SQL).
    """
    def __init__(self):
        self._history: list[ChatMessage] = []

    def add_message(self, role: str, content: str):
        """Validates and appends a message using Pydantic."""
        try:
            msg = ChatMessage(role=role, content=content)
            self._history.append(msg)
            logger.debug(f"Added {role} message to history.")
        except Exception as e:
            logger.error(f"Failed to add message to history: {e}")

    def get_history(self) -> list[ChatMessage]:
        return self._history

    def print_history(self):
        """Nicely prints the history sequence similar to the notebook."""
        print("\n" + "="*40 + " Chat History " + "="*40)
        for msg in self._history:
            print(f"[{msg.role.upper()}]: {msg.content}")
        print("=" * 94 + "\n")
