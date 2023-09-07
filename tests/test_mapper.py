from pathlib import Path
from ..pseudocode_summarizer.mapper import map_project_folder, remove_gitignored_files, ProjectFile
from typing import Generator
import pytest


@pytest.fixture
def setup_test_environment(tmp_path: Path) -> Generator[tuple[Path, list[ProjectFile]], any, None]:
    # Create some sample ProjectFile objects
    project_files = [
        ProjectFile(path=Path("file1.txt"), modified="2022-01-01 00:00:00"),
        ProjectFile(path=Path("file2.py"), modified="2022-01-01 00:00:00"),
        ProjectFile(path=Path("folder/file3.txt"), modified="2022-01-01 00:00:00"),
        ProjectFile(path=Path("folder/.gitignore"), modified="2022-01-01 00:00:00"),
        ProjectFile(path=Path(".gitignore"), modified="2022-01-01 00:00:00"),
        ProjectFile(path=Path("dir1/file2.txt"), modified="2022-01-01 00:00:00"),
        ProjectFile(path=Path("ignored_dir/file_in_ignored_dir.txt"), modified="2022-01-01 00:00:00")
    ]

    # Create files and directories based on project_files
    for pf in project_files:
        full_path = tmp_path / pf.path
        if full_path.name == ".gitignore" or full_path.suffix:  # It's a file
            full_path.parent.mkdir(parents=True, exist_ok=True)
            if full_path.name == ".gitignore":
                if full_path.parent == tmp_path:
                    full_path.write_text(data="*.txt\nignored_dir\n")
                elif full_path.parent == tmp_path / "folder":
                    full_path.write_text(data="file3.txt\n")
            else:
                full_path.write_text(data="")
        else:  # It's a directory
            full_path.mkdir(parents=True, exist_ok=True)

    yield tmp_path, project_files


def test_map_project_folder(setup_test_environment) -> None:
    # Unpack the test environment
    tmp_path, project_files = setup_test_environment

    # Run the function with the test directory as the startpath
    result: list[ProjectFile] = map_project_folder(startpath=tmp_path)

    # Sort both lists by the path attribute
    result = sorted(result, key=lambda x: x.path)
    expected_paths = sorted(project_files, key=lambda x: x.path)

    # Check that the lengths are the same
    assert len(result) == len(expected_paths)

    # Check only the paths, ignoring the modified timestamps
    for expected_path, actual_result in zip(expected_paths, result):
        assert expected_path.path == actual_result.path


def test_no_gitignore(setup_test_environment) -> None:
    tmp_path, project_files = setup_test_environment
    result = remove_gitignored_files(startpath=tmp_path, project_files=[ProjectFile(path=Path("file1.txt"), modified="2022-01-01 00:00:00")])
    assert len(result) == 1


def test_root_gitignore(setup_test_environment) -> None:
    tmp_path, project_files = setup_test_environment
    result = remove_gitignored_files(startpath=tmp_path, project_files=project_files)
    remaining_files = [file.path.name for file in result]
    assert "file2.py" in remaining_files
    assert "file1.txt" not in remaining_files


def test_subdir_gitignore(setup_test_environment) -> None:
    tmp_path, project_files = setup_test_environment
    result = remove_gitignored_files(startpath=tmp_path, project_files=project_files)
    remaining_files = [file.path.name for file in result if file.path.parent == Path("folder")]
    assert "file3.txt" not in remaining_files
