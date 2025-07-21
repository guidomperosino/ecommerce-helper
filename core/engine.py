# core/engine.py

from typing import Dict, Any
from adapters.ai_provider import AIProvider

class Engine:
    """
    Orchestrates the flow: incoming message → intent detection → data fetch → response.
    Uses direct formatting for known commands with data, and AI for others.

    Messages context stores items with 'role':
      - 'system': system instructions or injected data
      - 'user': messages from the user
      - 'assistant': AI or formatted responses
    """
    def __init__(
        self,
        adapters: Dict[str, Any],
        datasources: Dict[str, Any],
        ai_provider: AIProvider
    ):
        self.adapters = adapters
        self.datasources = datasources
        self.ai = ai_provider
        self.context: Dict[int, list] = {}  # chat_id → list of messages

    def handle_message(self, chat_id: int, text: str) -> str:
        # 1) Save user message to context
        self._add_to_context(chat_id, text, role='user')

        # 2) Detect intent and fetch data
        intent, data = self._detect_intent_and_fetch(text)

        # 3) If known intent with direct data, format without AI
        if data is not None:
            response = self._format_direct_response(intent, data)
        else:
            # 4) Build messages payload for AI
            messages = self._build_messages(chat_id)
            response = self.ai.ask(messages)

        # 5) Save assistant (or direct) response
        self._add_to_context(chat_id, response, role='assistant')
        return response

    def _add_to_context(self, chat_id: int, content: str, role: str):
        """
        Add a message to the conversation context.
        role must be 'system', 'user', or 'assistant'.
        """
        if chat_id not in self.context:
            self.context[chat_id] = []
        self.context[chat_id].append({'role': role, 'content': content})

    def _detect_intent_and_fetch(self, text: str):
        txt = text.lower()
        # Direct sales report
        if 'sales' in txt or 'ventas' in txt:
            data = self.datasources['meli'].get_sales(since_days=7)
            return 'sales', data
        # Direct stock query
        if 'stock' in txt:
            data = self.datasources['tienda_nube'].get_stock()
            return 'stock', data
        # No direct data command
        return 'default', None

    def _format_direct_response(self, intent: str, data: Any) -> str:
        """
        Format known-intent responses without calling AI.
        """
        if intent == 'sales':
            # Assume data is a number or summary string
            return f"You had {data} sales in the last 7 days."
        if intent == 'stock':
            # Assume data is a dict or list
            return f"Current stock:\n{data}"
        return str(data)

    def _build_messages(self, chat_id: int):
        """
        Build message list for AI, including system prompt and full chat history.
        """
        history = list(self.context.get(chat_id, []))
        # Load system prompt
        with open('prompts/system_prompt.txt', encoding='utf-8') as f:
            system_prompt = f.read().strip()
        # Prepend system prompt
        messages = [{'role': 'system', 'content': system_prompt}] + history
        return messages
