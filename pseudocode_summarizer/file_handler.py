# file_handler.py
from .datastructures import ModulePseudocode, ProjectFile
from pathlib import Path
from datetime import datetime


# Given a pseudocode.md file path, create a list of ModulePseudocode objects
# from the file or create the file and return an empty list if the file does
# not exist
def read_pseudocode_file(pseudocode_file: Path) -> list[ModulePseudocode]:
    # Create empty list
    pseudocode = []

    # If the pseudocode file does not exist, create it and return an empty list
    if not pseudocode_file.exists():
        pseudocode_file.touch()
        return pseudocode

    # Read the file
    with(open(file=pseudocode_file, mode="r")) as f:
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
        # Create a ModulePseudocode object and validate with Pydantic
        module = ModulePseudocode(path=path, modified=modified, content=content)
        #Append dict to the list
        pseudocode.append(module)
    
    # Return the list
    return pseudocode


# Given a list of ModulePseudocode objects, create a pseudocode.md file
def write_pseudocode_file(pseudocode: list[ModulePseudocode], pseudocode_file: Path) -> None:
    # Create empty string
    contents = ""

    # For each dict in the list, add a section to the string
    for module in pseudocode:
        # Add a single-hashed header with the path
        contents += "# " + str(object=module.path) + "\n"
        # Add the modified timestamp
        contents += str(object=module.modified) + "\n"
        # Add the content
        contents += module.content + "\n\n"
    
    # Write the string to the file
    if pseudocode:
        pseudocode_file.parent.mkdir(parents=True, exist_ok=True)
        with(open(file=pseudocode_file, mode="w")) as f:
            f.write(contents)


# Given a `pseudocode` list of ModulePseudocode objects and a `files` list of
# ProjectFile objects, filter the `project_files` list to output tuple of
# `new_files` missing from `pseudocode_file` and `modified_files` with
# 'modified' time stamps later than the 'modified' time stamps for the
# corresponding files in `pseudocode`.
def identify_new_and_modified_files(pseudocode: list[ModulePseudocode], project_files: list[ProjectFile]) -> tuple[list[ProjectFile], list[ProjectFile]]:
    # Create a mapping of 'path' to 'modified' from the pseudocode list
    pseudocode_map = {entry.path: entry.modified for entry in pseudocode}

    # Filter the files list
    new_files = []
    modified_files = []
    for file in project_files: 
        # If the path is not in the pseudocode map, add to new_files
        if file.path not in pseudocode_map:
            new_files.append(file)
        # If a file's 'modified' time is later than listed in the pseudocode
        # file, add to modified_files
        elif file.modified > pseudocode_map[file.path]:
            modified_files.append(file)

    # Return the filtered lists of dicts
    return new_files, modified_files


# Given a `pseudocode` list of ModulePseudocode objects and a `files` list of
# ProjectFile objects, filter the  `pseudocode` list to omit any files missing
# from `files`.
def remove_deleted_files_from_pseudocode(pseudocode: list[ModulePseudocode], files: list[ProjectFile]) -> list[ModulePseudocode]:
    # Convert the 'files' list into a set of paths for faster lookup
    file_paths = {file.path for file in files}

    # Filter the 'pseudocode' list to include only files present in 'files'
    filtered_pseudocode = [entry for entry in pseudocode if entry.path in file_paths]

    # Return the filtered list
    return filtered_pseudocode
