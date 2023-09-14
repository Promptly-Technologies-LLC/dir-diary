# test_classifier.py
from pathlib import Path
import pytest
import json
from dir_diary.datastructures import FileClassificationList, ProjectFile
from dir_diary.classifier import classify_files, initialize_project_map
from dir_diary.chatbot import LLMClient

@pytest.fixture
def setup_project_map_file(tmp_path) -> Path:
    project_map_path = tmp_path / "project_map.json"
    yield project_map_path

# Define pytest fixture for resetting singleton
@pytest.fixture
def reset_singleton():
    LLMClient._instance = None
    LLMClient._initialized = False
    yield


# Test initialize_project_map
def test_initialize_project_map_file_exists_and_well_formed(setup_project_map_file) -> None:
    # Create a temporary JSON file
    project_map_data = {
        "files": [
            {"path": ".gitignore", "role": "configuration"},
            # ... (other entries)
        ]
    }
    with open(file=setup_project_map_file, mode='w') as f:
        json.dump(obj=project_map_data, fp=f)
    
    # Call the function
    result = initialize_project_map(project_map_path=setup_project_map_file)
    
    # Validate the result
    assert len(result.files) == len(project_map_data['files'])
    assert result.files[0].path == Path(".gitignore")
    assert result.files[0].role == "configuration"


def test_initialize_project_map_file_exists_but_empty(setup_project_map_file) -> None:
    # Create an empty temporary JSON file
    setup_project_map_file.touch()
    
    # Call the function
    result = initialize_project_map(project_map_path=setup_project_map_file)
    
    # Validate the result
    assert len(result.files) == 0


def test_initialize_project_map_file_does_not_exist(setup_project_map_file) -> None:
    # Call the function
    result = initialize_project_map(project_map_path=setup_project_map_file)
    
    # Validate the result
    assert len(result.files) == 0


# Test classify_new_files
def test_classify_files(reset_singleton) -> None:
    # Create a test project map file and some example files
    project_map_file = Path("test_project_map.json")
    example_file_paths: list[str] = ["/foo/bar.py","/foo/helloworld.py","/README.md"]
    project_files: list[ProjectFile] = [ProjectFile(path=Path(path), modified=0) for path in example_file_paths]
    
    try:
        # Run classify_files
        project_map: list[ProjectFile] = classify_files(
                project_map_file=project_map_file,
                project_files=project_files
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
        assert FileClassificationList.model_validate_json(json_data=project_map_file_content)
    finally:
        # Delete the test_project_map.json file
        if project_map_file.exists():
            project_map_file.unlink()
