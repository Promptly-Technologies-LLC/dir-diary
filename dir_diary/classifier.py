from .file_handler import ProjectFile
from .langchain_chatbot import classify_with_langchain
from .datastructures import FileClassification, FileClassificationList
from pathlib import Path
import json


# Initialize a project map from a JSON file
def initialize_project_map(project_map_path: Path) -> FileClassificationList:
    # Initialize a default empty FileClassificationList
    project_map: FileClassificationList = FileClassificationList(files=[])
    
    # If project map file exists, get the project map from saved JSON file as a
    # FileClassificationList
    if project_map_path.exists():
        if project_map_path.stat().st_size == 0:
            # File exists but is empty, issue a warning return an empty project map
            print("Warning: The project map file is empty. Initializing an empty project map.")
            return project_map
        
        with open(file=project_map_path, mode='r') as f:
            project_map_json: list[dict] = json.load(fp=f)
            project_map: FileClassificationList = FileClassificationList.model_validate(obj=project_map_json)
    
    # Return the project map
    return project_map


# Update the project map with new files and remove deleted files
def update_project_map(
            project_map: FileClassificationList,
            project_files: list[ProjectFile]
        ) -> FileClassificationList:
    # Create a list of existing paths in project_map for easier lookup
    existing_paths = [existing_file.path for existing_file in project_map.files]
    
    # For any paths in project_files that are not in project_map, add them
    for new_file in project_files:
        if new_file.path not in existing_paths:
            project_map.files.append(FileClassification(path=new_file.path, role=None))
    
    # Remove any paths in project_map that are not in project_files
    project_map.files = [existing_file for existing_file in project_map.files if existing_file.path in [new_file.path for new_file in project_files]]

    # Return the updated project map
    return project_map


# Query a chatbot to determine the role that files play in the project
def classify_files(
            project_map_file: Path,
            project_files: list[ProjectFile]
        ) -> list[ProjectFile]:
    # Get the project map from JSON file or initialize an empty one
    project_map: FileClassificationList = initialize_project_map(
            project_map_path=project_map_file
        )
    
    # Add new files to project_map with None role and remove deleted files
    project_map: FileClassificationList = update_project_map(
            project_map=project_map,
            project_files=project_files
        )

    # If no project_map files have None role, get roles and return project_files
    if not any([file.role is None for file in project_map.files]):
        # Assign roles to project_files based on corresponding roles in project_map
        project_files: list[ProjectFile] = assign_roles(project_map=project_map, project_files=project_files)

        # Return the updated project_files
        return project_files

    # Convert the project_map to an input string
    input_str: str = project_map.to_json()

    # Query the LLM to update the project map
    project_map: FileClassificationList = classify_with_langchain(
                input_str=input_str,
            )

    # If project map is not empty, write it to the project_map_file
    if project_map:
        # Ensure parent directory exists
        project_map_file.parent.mkdir(parents=True, exist_ok=True)
        with open(file=project_map_file, mode="w") as f:         
            # Write the JSON-formatted project map to the file
            f.write(project_map.to_json())

    # Assign roles to project_files based on corresponding roles in project_map
    project_files: list[ProjectFile] = assign_roles(project_map=project_map, project_files=project_files)

    # Return the updated project map
    return project_files


# Assign roles to project files based on corresponding roles in project_map
def assign_roles(
            project_map: FileClassificationList,
            project_files: list[ProjectFile]
        ) -> list[ProjectFile]:
    # Create a mapping of project_files entries to project_map roles by path
    mapping: dict[Path, str] = {Path(file.path): file.role for file in project_map.files}

    # Use the mapping to add roles to project_files
    for file in project_files:
        file.role = mapping.get(file.path, None)

    # Return the updated project_files
    return project_files
