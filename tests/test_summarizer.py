import os
from pathlib import Path
import datetime
from pseudocode_summarizer import summarize_file, ProjectFile, initialize_model, ModulePseudocode
from langchain.chat_models import ChatOpenAI


# Test summarize_file
def test_summarize_file() -> None:
    input = "def foo():\n    print('Hello, world!')"
    with open(file="test_input.py", mode="w") as f:
        f.write(input)
    llm: ChatOpenAI = initialize_model(api_key=None, temperature=0, model_name='gpt-3.5-turbo')
    result = summarize_file(file_to_summarize=ProjectFile(path="test_input.py", modified=0), llm=llm)
    os.remove(path="test_input.py")

    expected_result = ModulePseudocode(
        path=Path('test_input.py'), modified=datetime.datetime(year=1970, month=1, day=1, hour=0, minute=0, tzinfo=datetime.timezone.utc), content='Function: foo\n\n1. Print "Hello, world!"'
    )

    assert result == expected_result
