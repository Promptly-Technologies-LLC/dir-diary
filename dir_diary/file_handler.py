# file_handler.py
from .datastructures import ModuleSummary, ProjectFile
from pathlib import Path
from datetime import datetime
from warnings import warn


# Given a summary file path, create a list of ModuleSummary objects
# from the file or create the file and return an empty list if the file does
# not exist
def read_summary_file(summary_file: Path) -> list[ModuleSummary]:
    # Initialize an empty list to hold ModuleSummary objects
    summaries: list[ModuleSummary] = []

    try:
        # Check if the summary_file exists
        if not summary_file.exists():
            # Create the file if it doesn't exist
            summary_file.touch()
            # Return an empty list as the file is newly created
            return summaries

        # Read the contents of the summary file
        with open(file=summary_file, mode="r") as f:
            contents: str = f.read()

        # Check if the content contains any sections, if not log a warning
        if "#" not in contents:
            warn(message="The summary file is empty or does not contain any recognizable sections.\nStarting fresh with a blank file.")
            summary_file.unlink()
            summary_file.touch()
            return []
        
        # Loop through each section in the file, separated by "# "
        # Skip the first section as it's empty
        for section in contents.split(sep="# ")[1:]:
            # Split the section into individual lines
            lines: list[str] = section.split(sep="\n")

            # Check if the section has at least 3 lines
            if len(lines) < 3:
                continue
            
            # Parse and type-hint individual parts of each section
            path: Path = Path(lines[0])
            modified: datetime = datetime.strptime(lines[1], "%Y-%m-%d %H:%M:%S")
            content: str = "\n".join(lines[2:]).rstrip("\n")
            
            # Create and validate a ModuleSummary object
            module: ModuleSummary = ModuleSummary(path=path, modified=modified, content=content)
            
            # Add the ModuleSummary object to the list
            summaries.append(module)
    
    except Exception as e:
        # Log a warning if an exception occurs
        warn(message=f"An error occurred while parsing the summary file: {e}\nStarting fresh with a blank file.")

        # Delete the file if it exists
        if summary_file.exists():
            summary_file.unlink()

        # Create a new empty file
        summary_file.touch()

        # Return an empty list since the original file was unparseable
        return []
    
    # Return the list of ModuleSummary objects
    return summaries


# Given a list of ModuleSummary objects, create a summary markdown file
def write_summary_file(summaries: list[ModuleSummary], summary_file: Path) -> None:    
    # Create empty string
    contents = ""

    # For each dict in the list, add a section to the string
    for module in summaries:
        # Add a single-hashed header with the path
        contents += "# " + str(object=module.path) + "\n"
        # Add the modified timestamp
        contents += str(object=module.modified) + "\n"
        # Add the content
        contents += module.content + "\n\n"
    
    # Write the string to the file
    if summaries:
        summary_file.parent.mkdir(parents=True, exist_ok=True)
        with(open(file=summary_file, mode="w")) as f:
            f.write(contents)


# Given a `summaries` list of ModuleSummary objects and a `files` list of
# ProjectFile objects, filter the `project_files` list to output tuple of
# `new_files` missing from `summary_file` and `modified_files` with
# 'modified' time stamps later than the 'modified' time stamps for the
# corresponding files in `summaries`.
def identify_new_and_modified_files(summaries: list[ModuleSummary], project_files: list[ProjectFile]) -> tuple[list[ProjectFile], list[ProjectFile]]:
    # Create a mapping of 'path' to 'modified' from the summaries list
    summaries_map = {entry.path: entry.modified for entry in summaries}

    # Filter the files list
    new_files = []
    modified_files = []
    for file in project_files: 
        # If the path is not in the summaries map, add to new_files
        if file.path not in summaries_map:
            new_files.append(file)
        # If a file's 'modified' time is later than listed in the summaries
        # file, add to modified_files
        elif file.modified > summaries_map[file.path]:
            modified_files.append(file)

    # Return the filtered lists of dicts
    return new_files, modified_files


# Given a `summaries` list of ModuleSummary objects and a `files` list of
# ProjectFile objects, filter the  `summaries` list to omit any files missing
# from `files`.
def remove_deleted_files_from_summaries(summaries: list[ModuleSummary], files: list[ProjectFile]) -> list[ModuleSummary]:
    # Convert the 'files' list into a set of paths for faster lookup
    file_paths = {file.path for file in files}

    # Filter the 'summaries' list to include only files present in 'files'
    filtered_summaries = [entry for entry in summaries if entry.path in file_paths]

    # Return the filtered list
    return filtered_summaries
