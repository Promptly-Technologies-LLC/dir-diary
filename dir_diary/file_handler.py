# file_handler.py
from .datastructures import ModuleSummary, ProjectFile
from pathlib import Path
from datetime import datetime


# Given a summary file path, create a list of ModuleSummary objects
# from the file or create the file and return an empty list if the file does
# not exist
def read_summary_file(summary_file: Path) -> list[ModuleSummary]:
    # Create empty list
    summaries = []

    # If the summary file does not exist, create it and return an empty list
    if not summary_file.exists():
        summary_file.touch()
        return summaries

    # Read the file
    with(open(file=summary_file, mode="r")) as f:
        contents = f.read()
    
    # For each section introduced by a single-hashed header, add a dict to the list
    # Skip the first (empty) section
    for section in contents.split(sep="# ")[1:]:
        # Split the section into lines
        lines = section.split(sep="\n")
        # Check that there are enough lines
        if len(lines) < 3:
            continue
        # The path is the first line
        path = Path(lines[0])
        # Convert the modified timestamp to a datetime object
        modified = datetime.strptime(lines[1], "%Y-%m-%d %H:%M:%S")
        # The content is the rest of the lines
        content = "\n".join(lines[2:]).rstrip("\n")
        # Create a ModuleSummary object and validate with Pydantic
        module = ModuleSummary(path=path, modified=modified, content=content)
        #Append dict to the list
        summaries.append(module)
    
    # Return the list
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
