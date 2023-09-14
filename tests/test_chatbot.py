import pytest
from dir_diary.chatbot import LLMClient

# Define pytest fixture for resetting singleton
@pytest.fixture
def reset_singleton():
    LLMClient._instance = None
    LLMClient._initialized = False
    yield

class TestLLMClient:

    # Use the fixture in the test methods
    def test_singleton_implementation(self, reset_singleton):
        client1 = LLMClient(api_key='key1', model_name='gpt-4', long_context_fallback="gpt-4-32k", temperature=0.7, total_cost=100)
        client2 = LLMClient(api_key='key2', model_name='gpt-3', long_context_fallback="gpt-3-16k", temperature=0.2, total_cost=50)
        
        assert client1 is client2
        assert client1._instance is client2._instance

    def test_no_overwrite_on_second_instantiation(self, reset_singleton) -> None:
        client1 = LLMClient(api_key='key1', model_name='gpt-4', long_context_fallback="gpt-4-32k", temperature=0.7, total_cost=100)
        client2 = LLMClient(api_key='key2', model_name='gpt-3', long_context_fallback="gpt-3-16k", temperature=0.2, total_cost=50)

        assert client1.api_key == 'key1' and client2.api_key == 'key1'
        assert client1.model_name == 'gpt-4' and client2.model_name == 'gpt-4'
        assert client1.long_context_fallback == 'gpt-4-32k' and client2.long_context_fallback == 'gpt-4-32k'
        assert client1.temperature == 0.7 and client2.temperature == 0.7
        assert client1.total_cost == 100 and client2.total_cost == 100
