import os
import pathspec
from pathlib import Path
from datetime import datetime
from .file_handler import ProjectFile


# Given a path to a project folder, map the folder and output a list of ProjectFile objects
def map_project_folder(startpath=".") -> list[ProjectFile]:
    # Convert startpath to a Path object
    startpath = Path(startpath)
    # Initialize a list to store the paths and modifications
    paths_and_modifications = []

    # Walk the directory tree
    for root, _, files in os.walk(top=startpath):
        # Add files to the list
        for f in files:
            file_path = Path(root) / f
            relative_file_path = file_path.relative_to(startpath)
            modified_time = datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            paths_and_modifications.append(ProjectFile(path=relative_file_path, modified=modified_time))

    # Return the list
    return paths_and_modifications


def remove_gitignored_files(startpath=".", project_files: list[ProjectFile]=ProjectFile(path=Path(".gitignore"), modified=datetime.now())) -> list[ProjectFile]:    
    # Convert startpath to a Path object
    startpath = Path(startpath)
    
    # Get a list of all .gitignore files in the project
    gitignore_files: list[ProjectFile] = [file for file in project_files if file.path.name == ".gitignore"]

    # Initialize an empty list to store the filtered files
    filtered_files = project_files.copy()
    
    # Iterate over the .gitignore files
    for file in gitignore_files:
        # Get the directory containing the .gitignore file
        gitignore_dir = file.path.parent

        # Read the .gitignore file
        with open(file=startpath / file.path, mode="r") as f:
            lines = f.readlines()
        
        # Create a pathspec object for this .gitignore file
        spec = pathspec.GitIgnoreSpec.from_lines(lines=lines)
        
        # Get the subset of project_files that are in the .gitignore file's
        # directory tree
        same_dir_files = [f for f in filtered_files if gitignore_dir in f.path.parents]
        
        # Get the subset of same_dir_files that match the spec
        to_remove = [f for f in same_dir_files if spec.match_file(f.path)]
        
        # Remove the matching files from filtered_files
        filtered_files = [f for f in filtered_files if f not in to_remove]
    
    # Return the filtered list
    return filtered_files


if __name__ == "__main__":
    from dir_diary.mapper import map_project_folder
    
    paths_list = map_project_folder(startpath=".")
    for entry in paths_list:
        print(entry["path"], entry["modified"])
