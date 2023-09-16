import pytest
from dir_diary.client import LLMClient

# Define pytest fixture for resetting singleton
@pytest.fixture
def reset_singleton():
    LLMClient._instance = None
    LLMClient._initialized = False
    yield

# Define pytest fixture for mocking validate_api_key
@pytest.fixture
def mock_validate_api_key(mocker):
    return mocker.patch('dir_diary.client.validate_api_key', side_effect=lambda api_key: api_key)

# Define pytest fixture for mocking validate_temperature
@pytest.fixture
def mock_validate_temperature(mocker):
    return mocker.patch('dir_diary.client.validate_temperature', side_effect=lambda temperature: temperature)


def test_singleton_implementation(reset_singleton, mock_validate_api_key, mock_validate_temperature) -> None:       
    client1 = LLMClient(api_key="key1", model_name='gpt-4', long_context_fallback="gpt-4-32k", temperature=0.7, total_cost=100)
    client2 = LLMClient(api_key="key2", model_name='gpt-3', long_context_fallback="gpt-3-16k", temperature=0.2, total_cost=50)
    
    assert client1 is client2
    assert client1._instance is client2._instance


def test_no_overwrite_on_second_instantiation(reset_singleton, mock_validate_api_key, mock_validate_temperature) -> None:
    client1 = LLMClient(api_key="key1", model_name='gpt-4', long_context_fallback="gpt-4-32k", temperature=0.7, total_cost=100)
    client2 = LLMClient(api_key="key2", model_name='gpt-3', long_context_fallback="gpt-3-16k", temperature=0.2, total_cost=50)

    assert client1.api_key is "key1" and client2.api_key is "key1"
    assert client1.model_name == 'gpt-4' and client2.model_name == 'gpt-4'
    assert client1.long_context_fallback == 'gpt-4-32k' and client2.long_context_fallback == 'gpt-4-32k'
    tolerance = 1e-9
    assert abs(client1.temperature - 0.7) < tolerance and abs(client2.temperature - 0.7) < tolerance
    assert client1.total_cost == 100 and client2.total_cost == 100


def test_validates_api_key(reset_singleton, mock_validate_api_key, mock_validate_temperature) -> None:      
    LLMClient(api_key="some_value", model_name='gpt-4', long_context_fallback="gpt-4-32k", temperature=0.7, total_cost=100)

    mock_validate_api_key.assert_called_once_with(api_key="some_value")


def test_validates_temperature(reset_singleton, mock_validate_api_key, mock_validate_temperature) -> None:       
    LLMClient(api_key="some_value", model_name='gpt-4', long_context_fallback="gpt-4-32k", temperature=0.7, total_cost=100)

    mock_validate_temperature.assert_called_once_with(temperature=0.7)
