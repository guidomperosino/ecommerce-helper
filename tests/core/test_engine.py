# tests/core/test_engine.py

import pytest
from core.engine import Engine
from pathlib import Path

class DummyDataSource:
    def __init__(self, value):
        self.value = value

    def get_sales(self, since_days):
        return self.value

    def get_stock(self):
        return self.value

class DummyAI:
    def __init__(self, answer):
        self.answer = answer
        self.messages = None

    def ask(self, messages):
        self.messages = messages
        return self.answer

@pytest.fixture
def engine_with_mocks():
    # Ensure prompts directory and system_prompt.txt exist
    prompts_dir = Path('prompts')
    prompts_dir.mkdir(exist_ok=True)
    (prompts_dir / 'system_prompt.txt').write_text('System: You are a test assistant.')

    # Prepare mocks
    adapters = {}
    datasources = {
        'meli': DummyDataSource(7),
        'tienda_nube': DummyDataSource({'apple': 10})
    }
    ai = DummyAI('AI says hello')
    engine = Engine(adapters=adapters, datasources=datasources, ai_provider=ai)
    return engine, ai


def test_sales_intent_direct(engine_with_mocks):
    engine, _ = engine_with_mocks
    response = engine.handle_message(chat_id=1, text='How many sales did I have today?')
    assert response == 'You had 7 sales in the last 7 days.'
    # Context stores user and assistant messages
    assert engine.context[1][0]['role'] == 'user'
    assert engine.context[1][1]['role'] == 'assistant'


def test_stock_intent_direct(engine_with_mocks):
    engine, _ = engine_with_mocks
    response = engine.handle_message(chat_id=2, text='Check stock please')
    assert 'Current stock:' in response
    assert 'apple' in response
    assert len(engine.context[2]) == 2


def test_ai_fallback(engine_with_mocks):
    engine, ai = engine_with_mocks
    response = engine.handle_message(chat_id=3, text='Tell me a joke')
    assert response == 'AI says hello'
    # Verify AI messages payload
    assert ai.messages[0]['role'] == 'system'
    assert 'System: You are a test assistant.' in ai.messages[0]['content']
    assert ai.messages[1]['role'] == 'user'
    assert ai.messages[1]['content'] == 'Tell me a joke'
