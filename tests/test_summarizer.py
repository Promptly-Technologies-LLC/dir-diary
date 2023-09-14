import pytest
import os
from pathlib import Path
import datetime
from dir_diary.summarizer import summarize_file
from dir_diary.datastructures import ModuleSummary, ProjectFile
from dir_diary.chatbot import LLMClient


# Define pytest fixture for resetting singleton
@pytest.fixture
def reset_singleton():
    LLMClient._instance = None
    LLMClient._initialized = False
    yield

# Test summarize_file
def test_summarize_file(reset_singleton) -> None:
    # Initialize LLMClient to get config and track cost
    client = LLMClient()
    
    # Create a test input file
    input = "def foo():\n    print('Hello, world!')"
    with open(file="test_input.py", mode="w") as f:
        f.write(input)
    
    try:
        # Define function arguments
        file_to_summarize = ProjectFile(path="test_input.py", modified=0)
        
        # Run summarize_file
        pseudocode_result = summarize_file(file_to_summarize=file_to_summarize, summary_type="pseudocode")
        initial_cost = client.total_cost

        usage_result = summarize_file(file_to_summarize=file_to_summarize, summary_type="usage")
        final_cost = client.total_cost
    finally:
        # Delete the test input file
        os.remove(path="test_input.py")

    # Define expected result
    expected_path = Path('test_input.py')
    expected_modified=datetime.datetime(year=1970, month=1, day=1, hour=0, minute=0, tzinfo=datetime.timezone.utc)
    expected_content=["print","hello"]

    # Assert that the result is an object of class ModuleSummary
    assert isinstance(pseudocode_result, ModuleSummary)
    assert isinstance(usage_result, ModuleSummary)

    # Assert that path and modified are as expected
    assert pseudocode_result.path == expected_path
    assert pseudocode_result.modified == expected_modified
    assert usage_result.path == expected_path
    assert usage_result.modified == expected_modified

    # Assert that content contains the case-agnostic words "print" and "hello"
    assert all([word in pseudocode_result.content.lower() for word in expected_content])
    assert all([word in usage_result.content.lower() for word in expected_content])

    # Assert that pseudocode and usage content are different
    assert pseudocode_result.content != usage_result.content

    # Assert that the cost after the second call is greater than after the first
    assert final_cost > initial_cost
