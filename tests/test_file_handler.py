# test_file_handler.py
from dir_diary.file_handler import read_summary_file, write_summary_file, identify_new_and_modified_files, remove_deleted_files_from_summaries
from dir_diary.datastructures import ModuleSummary, ProjectFile
from pathlib import Path
from datetime import datetime
import os


def test_read_and_write_summary_file(tmp_path) -> None:
    # Test when pseudocode file does not exist
    non_existent_file: Path = tmp_path / "non_existent.md"
    pseudocode = read_summary_file(summary_file=non_existent_file)
    assert pseudocode == []
    assert non_existent_file.exists()

    # Create a temporary pseudocode file
    pseudocode_file: Path = tmp_path / "pseudocode.md"
    pseudocode_file.write_text("# /path/to/file\n2022-01-01 00:00:00\nThis is the content\n")

    # Read the pseudocode file
    pseudocode: list[ModuleSummary] = read_summary_file(summary_file=pseudocode_file)

    # Create an expected ModuleSummary object
    expected_pseudocode = ModuleSummary(
        path=Path("/path/to/file"),
        modified=datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0),
        content="This is the content"
    )

    # Check the contents of the pseudocode list
    assert pseudocode == [expected_pseudocode]

    # Write the pseudocode list back to a new file
    new_pseudocode_file = tmp_path / "new_pseudocode.md"
    write_summary_file(summaries=pseudocode, summary_file=new_pseudocode_file)

    # Read the new pseudocode file
    new_pseudocode_list = read_summary_file(summary_file=new_pseudocode_file)

    # Check the contents of the new pseudocode list
    assert new_pseudocode_list == [expected_pseudocode]


def test_read_and_write_multiple_sections(tmp_path) -> None:
    # Create a temporary pseudocode file with multiple sections
    pseudocode_file = tmp_path / "pseudocode.md"
    pseudocode_file.write_text("# /path/to/file1\n2022-01-01 00:00:00\nContent 1\n# /path/to/file2\n2022-02-02 00:00:00\nContent 2\n")

    # Read the pseudocode file
    pseudocode_list = read_summary_file(summary_file=pseudocode_file)

    # Create expected ModuleSummary instances
    module1 = ModuleSummary(
        path=Path("/path/to/file1"),
        modified=datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0),
        content="Content 1"
    )
    module2 = ModuleSummary(
        path=Path("/path/to/file2"),
        modified=datetime(year=2022, month=2, day=2, hour=0, minute=0, second=0),
        content="Content 2"
    )

    # Check the contents of the pseudocode list
    expected = [module1, module2]
    assert pseudocode_list == expected


def test_identify_new_and_modified_files(tmp_path) -> None:
    # Create a temporary pseudocode file
    pseudocode_file: Path = tmp_path / "pseudocode.md"
    pseudocode_file.write_text("# file1.txt\n2023-08-20 00:00:00\nContent 1\n# file2.txt\n2023-08-21 00:00:00\nContent 2\n")

    # Read the pseudocode file to generate the pseudocode list
    pseudocode = read_summary_file(summary_file=pseudocode_file)

    try:
        # Test data using Pydantic's ProjectFile
        project_files = [
            ProjectFile(path=Path("file1.txt"), modified=datetime(year=2023, month=8, day=19, hour=0, minute=0, second=0)),
            ProjectFile(path=Path("file2.txt"), modified=datetime(year=2023, month=8, day=22, hour=0, minute=0, second=0)),
            ProjectFile(path=Path("file3.txt"), modified=datetime(year=2023, month=8, day=22, hour=0, minute=0, second=0))
        ]

        # Expected result using Pydantic's ProjectFile
        expected_new_files = [
            ProjectFile(path=Path("file3.txt"), modified=datetime(year=2023, month=8, day=22, hour=0, minute=0, second=0))
        ]
        expected_modified_files = [
            ProjectFile(path=Path("file2.txt"), modified=datetime(year=2023, month=8, day=22, hour=0, minute=0, second=0))
        ]

        # Call the identify_new_and_modified_files function
        new_files, modified_files = identify_new_and_modified_files(summaries=pseudocode, project_files=project_files)

        # Assert the result using Pydantic objects
        assert new_files == expected_new_files, f"Expected new_files to be {expected_new_files}, but got {new_files}"
        assert modified_files == expected_modified_files, f"Expected modified_files to be {expected_modified_files}, but got {modified_files}"

    finally:
        # Cleanup: Remove the temporary pseudocode file
        os.remove(path=pseudocode_file)


def test_remove_deleted_files_from_summaries() -> None:
    # Test data
    dt1 = datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0)
    dt2 = datetime(year=2022, month=2, day=1, hour=0, minute=0, second=0)
    dt3 = datetime(year=2022, month=3, day=1, hour=0, minute=0, second=0)
    
    pseudocode = [
        ModuleSummary(path="file1.txt", modified=dt1, content="content1"),
        ModuleSummary(path="file2.txt", modified=dt2, content="content2"),
        ModuleSummary(path="file3.txt", modified=dt3, content="content3")
    ]
    files = [
        ProjectFile(path="file1.txt", modified=datetime.now()),
        ProjectFile(path="file3.txt", modified=datetime.now())
    ]

    # Expected result
    expected_filtered_pseudocode = [
        ModuleSummary(path="file1.txt", modified=dt1, content="content1"),
        ModuleSummary(path="file3.txt", modified=dt3, content="content3")
    ]

    # Call the function
    actual_filtered_pseudocode = remove_deleted_files_from_summaries(summaries=pseudocode, files=files)

    # Assert the result
    assert actual_filtered_pseudocode == expected_filtered_pseudocode, f"Expected {expected_filtered_pseudocode}, but got {actual_filtered_pseudocode}"
