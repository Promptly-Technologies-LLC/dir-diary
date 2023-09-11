import os
from pathlib import Path
import datetime
from pseudocode_summarizer.summarizer import summarize_file
from pseudocode_summarizer.datastructures import ModulePseudocode, ProjectFile
from pseudocode_summarizer.chatbot import initialize_model
from langchain.chat_models import ChatOpenAI


# Test summarize_file
def test_summarize_file() -> None:
    # Create a test input file
    input = "def foo():\n    print('Hello, world!')"
    with open(file="test_input.py", mode="w") as f:
        f.write(input)
    
    try:
        # Define function arguments
        file_to_summarize = ProjectFile(path="test_input.py", modified=0)
        llm: ChatOpenAI = initialize_model(api_key=None, temperature=0, model_name="gpt-3.5-turbo")
        long_context_llm: ChatOpenAI = initialize_model(api_key=None, temperature=0, model_name="gpt-3.5-turbo-16k")
        
        # Run summarize_file
        result = summarize_file(file_to_summarize=file_to_summarize, llm=llm, long_context_llm=long_context_llm)
    finally:
        # Delete the test input file
        os.remove(path="test_input.py")

    # Define expected result
    expected_path = Path('test_input.py')
    expected_modified=datetime.datetime(year=1970, month=1, day=1, hour=0, minute=0, tzinfo=datetime.timezone.utc)
    expected_content=["print","hello"]

    # Assert that the result is an object of class ModulePseudocode
    assert isinstance(result, ModulePseudocode)

    # Assert that path and modified are as expected
    assert result.path == expected_path
    assert result.modified == expected_modified

    # Assert that content contains the case-agnostic words "print" and "hello"
    assert all([word in result.content.lower() for word in expected_content])
