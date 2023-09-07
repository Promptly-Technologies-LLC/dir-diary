import os
from pathlib import Path
import datetime
from pseudocode_summarizer import summarize_file, ProjectFile, initialize_model, ModulePseudocode
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import OpenAICallbackHandler


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
        callback_handler = OpenAICallbackHandler()
        
        # Run summarize_file
        result = summarize_file(file_to_summarize=file_to_summarize, llm=llm, long_context_llm=long_context_llm, callbacks=[callback_handler])
    finally:
        # Delete the test input file
        os.remove(path="test_input.py")

    # Define expected result
    expected_result = ModulePseudocode(
        path=Path('test_input.py'), modified=datetime.datetime(year=1970, month=1, day=1, hour=0, minute=0, tzinfo=datetime.timezone.utc), content="Define a function named foo\n\n    Print the string 'Hello, world!'"
    )

    # Assert that the result is as expected
    assert result == expected_result
