from dir_diary.openai_chatbot import (
        calculate_cost, query_llm, summarize_with_openai, classify_with_openai,
        functions, file_classification_prompt, pseudocode_prompt, usage_prompt
    )
from dir_diary.client import LLMClient
from dir_diary.datastructures import FileClassification, FileClassificationList
import pytest
from openai import InvalidRequestError

short_context_response = {
            "id": "chatcmpl-7zDM96XteqdNQPFz4ROKcixFDnLSR",
            "object": "chat.completion",
            "created": 1694823705,
            "model": "gpt-3.5-turbo-0613",
            "choices": [
                {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello! How can I help you today?"
                },
                "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 9,
                "completion_tokens": 9,
                "total_tokens": 18
            }
        }

long_context_response = {
            "id": "chatcmpl-7zDM96XteqdNQPFz4ROKcixFDnLSR",
            "object": "chat.completion",
            "created": 1694823705,
            "model": "gpt-3.5-turbo-16k-0613",
            "choices": [
                {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello! How can I help you today?"
                },
                "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 9,
                "completion_tokens": 9,
                "total_tokens": 18
            }
        }

functions_response = {
  "id": "chatcmpl-7zTiJWTYXoIYQaY1ZxC9SVCzyPbHp",
  "object": "chat.completion",
  "created": 1694886583,
  "model": "gpt-3.5-turbo-0613",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": None,
        "function_call": {
          "name": "classify_project_files_by_role",
          "arguments": "{\n  \"files\": [\n    {\n      \"path\": \"/foo/bar.py\",\n      \"role\": \"source\"\n    },\n    {\n      \"path\": \"/foo/helloworld.py\",\n      \"role\": \"source\"\n    },\n    {\n      \"path\": \"/README.md\",\n      \"role\": \"documentation\"\n    }\n  ]\n}"
        }
      },
      "finish_reason": "function_call"
    }
  ],
  "usage": {
    "prompt_tokens": 328,
    "completion_tokens": 79,
    "total_tokens": 407
  }
}

example_file_paths: list[str] = ["\\foo\\bar.py", "\\foo\\helloworld.py", "\\README.md"]
files_to_classify: list[FileClassification] = [FileClassification(path=path, role=None) for path in example_file_paths]
files_to_classify: FileClassificationList = FileClassificationList(files=files_to_classify)

# Define pytest fixture for resetting singleton
@pytest.fixture
def reset_singleton():
    LLMClient._instance = None
    LLMClient._initialized = False
    yield

# Define pytest fixture for mocking response from openai.ChatCompletion.create
# depending on whether `model` argument is 'gpt-3.5-turbo' or 'gpt-3.5-turbo-16k'
@pytest.fixture
def mock_response(monkeypatch) -> None:
    def mock_create(*args, **kwargs):
        model = kwargs.get("model")
        messages = kwargs.get("messages")
        functions = kwargs.get("functions")
        function_call = kwargs.get("function_call")
        max_tokens = kwargs.get("max_tokens")

        # If 'functions' is not passed at all, it will be None
        if (
                model == "gpt-3.5-turbo" and
                messages == [{"role": "user", "content": "hello"}] and
                functions is None and
                function_call is None and
                isinstance(max_tokens, int)
        ):
            return short_context_response
        if (
                model == "gpt-3.5-turbo" and
                messages == [{"role": "user", "content": "This is a long prompt"}] and
                functions is None and
                function_call is None and
                isinstance(max_tokens, int)
        ):
            raise InvalidRequestError(message="Too many tokens requested", param="max_tokens")
        elif (
                model == "gpt-3.5-turbo-16k" and
                messages == [{"role": "user", "content": "This is a long prompt"}] and
                functions is None and
                function_call is None and
                isinstance(max_tokens, int)
        ):
            return long_context_response
        elif (
                model == "gpt-3.5-turbo" and
                messages == [{"role": "user", "content": file_classification_prompt % ", ".join(example_file_paths)}] and
                functions is functions and
                function_call == {'name': functions[0]['name']} and
                isinstance(max_tokens, int)
        ):
            return functions_response
        else:
            raise ValueError("Unexpected arguments passed to openai.ChatCompletion.create")

    monkeypatch.setattr("openai.ChatCompletion.create", mock_create)


def test_calculate_cost() -> None:    
    tolerance = 0.000001
    prompt_cost_per_token = 0.0015/1000
    completion_cost_per_token = 0.002/1000
    assert abs(calculate_cost(response=short_context_response) - (9 * prompt_cost_per_token + 9 * completion_cost_per_token)) < tolerance


def test_query_llm_with_short_context(reset_singleton, mock_response, mocker) -> None:
    LLMClient(api_key=None, model_name='gpt-3.5-turbo', long_context_fallback="gpt-3.5-turbo-16k", temperature=0.7, total_cost=0)
    
    mock_get_max_tokens = mocker.patch('dir_diary.openai_chatbot.get_max_tokens', return_value=2000)
    
    # Test with short prompt
    response = query_llm(prompt="hello")

    assert isinstance(response, dict)
    assert response == short_context_response

    mock_get_max_tokens.assert_called_once_with(long=False)


def test_query_llm_with_long_context(reset_singleton, mock_response, mocker) -> None:
    LLMClient(api_key=None, model_name='gpt-3.5-turbo', long_context_fallback="gpt-3.5-turbo-16k", temperature=0.7, total_cost=0)
    
    mock_get_max_tokens = mocker.patch('dir_diary.openai_chatbot.get_max_tokens', return_value=8000)
    
    # Test with long prompt
    response = query_llm(prompt="This is a long prompt")

    assert isinstance(response, dict)
    assert response == long_context_response

    calls = [mocker.call(long=False), mocker.call(long=True)]
    mock_get_max_tokens.assert_has_calls(calls, any_order=False)


def test_query_llm_with_functions(reset_singleton, mock_response) -> None:
    # Initialize the client
    LLMClient(api_key=None, model_name='gpt-3.5-turbo', long_context_fallback="gpt-3.5-turbo-16k", temperature=0.7, total_cost=0)

    # Test with file classification prompt and comma-separated list of paths
    prompt = file_classification_prompt % ", ".join(example_file_paths)
    
    # Test with functions
    response = query_llm(prompt=prompt, functions=functions)
    
    # Parse the response
    json_response = response['choices'][0]['message']['function_call']['arguments']
    parsed_response = FileClassificationList.model_validate_json(json_data=json_response)

    assert isinstance(parsed_response, FileClassificationList)
    assert isinstance(response, dict)
    assert all([file.role is not None for file in parsed_response.files])

    # When I call the LLM with a prompt containing a list of file paths and
    # Explicit instructions not to allow None or null values, it works. But
    # if I give it a prompt that looks too much like the data structure I'm
    # asking for, it echoes it back to me with null values even if I disallow
    # them. 
    #
    # prompt = file_classification_prompt % files_to_classify.to_json()
    # 
    # Also, if I give it a list of file paths without instructions not
    # to allow null values, it gives me some null values even if these aren't
    # allowed by the Pydantic schema. Worth a writeup.

def test_summarize_with_openai(reset_singleton, mocker) -> None:
    LLMClient(api_key=None, model_name='gpt-3.5-turbo', long_context_fallback="gpt-3.5-turbo-16k", temperature=0.7, total_cost=0)
    
    input_str = "hello"
    
    # Test with pseudocode prompt
    mock_query_llm = mocker.patch('dir_diary.openai_chatbot.query_llm', return_value=short_context_response)
    str_response: str = summarize_with_openai(input_str=input_str, summary_type="pseudocode")
    assert str_response == "Hello! How can I help you today?"
    mock_query_llm.assert_called_once_with(prompt=pseudocode_prompt % input_str)

    # Test with usage prompt
    mock_query_llm = mocker.patch('dir_diary.openai_chatbot.query_llm', return_value=short_context_response)
    str_response: str = summarize_with_openai(input_str=input_str, summary_type="usage")
    assert str_response == "Hello! How can I help you today?"
    mock_query_llm.assert_called_once_with(prompt=usage_prompt % input_str)


def test_classify_with_openai(reset_singleton, mocker) -> None:
    LLMClient(api_key=None, model_name='gpt-3.5-turbo', long_context_fallback="gpt-3.5-turbo-16k", temperature=0.7, total_cost=0)
    
    # Test with file classification prompt and comma-separated list of paths
    prompt = file_classification_prompt % ", ".join(example_file_paths)
    
    # Test with functions
    mock_query_llm = mocker.patch('dir_diary.openai_chatbot.query_llm', return_value=functions_response)
    project_map = classify_with_openai(project_map=files_to_classify)
    mock_query_llm.assert_called_once_with(
        prompt=prompt,
        functions=functions
    )

    assert isinstance(project_map, FileClassificationList)
    assert all([file.role is not None for file in project_map.files])
