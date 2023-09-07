# test_classifier.py
from pathlib import Path
from pseudocode_summarizer import (classify_files, initialize_model,
                                   ProjectFile, FileClassificationList)
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import OpenAICallbackHandler


# Test classify_new_files
def test_classify_files() -> None:
    # Create a test project map file and some example files
    project_map_file = Path("test_project_map.json")
    example_file_paths: list[str] = ["/foo/bar.py","/foo/helloworld.py","/README.md"]
    project_files: list[ProjectFile] = [ProjectFile(path=Path(path), modified=0) for path in example_file_paths]
    
    try:
        # Define function arguments
        llm: ChatOpenAI = initialize_model(api_key=None, temperature=0, model_name="gpt-3.5-turbo")
        long_context_llm: ChatOpenAI = initialize_model(api_key=None, temperature=0, model_name="gpt-3.5-turbo-16k")
        callback_handler = OpenAICallbackHandler()

        # Run classify_files
        project_map: list[ProjectFile] = classify_files(
                project_map_file=project_map_file,
                project_files=project_files,
                llm=llm,
                long_context_llm=long_context_llm,
                callbacks=[callback_handler]
            )
    
        # Check that the project map is as expected: "source" for ".py" files,
        # documentation for ".md"
        expected_result = [ProjectFile(path=Path(path), modified=0, role="source") for path in example_file_paths if path.endswith(".py")]
        expected_result += [ProjectFile(path=Path(path), modified=0, role="documentation") for path in example_file_paths if path.endswith(".md")]
        assert project_map == expected_result

        # Check that the test_project_map.json file was created and validate
        # that content can be parsed as FileClassificationList
        with open(file=project_map_file, mode="r") as f:
            project_map_file_content = f.read()
        assert FileClassificationList.parse_raw(b=project_map_file_content)
    finally:
        # Delete the test_project_map.json file
        if project_map_file.exists():
            project_map_file.unlink()