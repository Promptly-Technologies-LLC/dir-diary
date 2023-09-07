from .file_handler import ProjectFile
from .chatbot import query_llm
from pathlib import Path
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
import json
from typing import Literal, Optional
from pydantic import BaseModel, Field

# Data structure for LLM classification of project file roles
class FileClassification(BaseModel):
    path: Path = Field(description="file path relative to the project root")
    role: Optional[Literal[
            "source", "configuration", "build or deployment", "documentation",
            "testing", "database", "utility scripts", "assets or data",
            "specialized"
        ]] = Field(
                default=None, description="role the file plays in the project"
            )

# Data structure for a list of FileClassifications
class FileClassificationList(BaseModel):
    files: list[FileClassification] = Field(
            description="List of file classifications"
        )
    
    # Method to convert a FileClassificationList to a JSON-formatted string
    def to_json(self) -> str:
        data_dict = self.dict(exclude_unset=True)
        
        # Convert Path objects to str
        for file in data_dict.get("files", []):
            file["path"] = str(object=file["path"])
        
        return json.dumps(obj=data_dict)


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
            project_map: FileClassificationList = FileClassificationList.parse_obj(obj=project_map_json)
    
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


# Parser for the LLM output
parser = PydanticOutputParser(pydantic_object=FileClassificationList)

# Prompt template for determining the roles that files play in the project
file_classification_prompt: PromptTemplate = PromptTemplate(
    template="We have mapped the file structure of a project folder for an existing coding project. Based solely on the file structure, let's attempt to classify them by the role they play in the project. We will label code modules, entry points, and endpoints as 'source'; config files, environment files, and dependency files as 'configuration'; build files, Docker files, and CI/CD files as 'build or deployment'; READMEs, CHANGELOGs, pseudocodes, project maps, licenses, and docs as 'documentation'; unit tests as 'testing'; migration, schema, and seed files as 'database', utility and action scripts as 'utility scripts', static assets like images, CSS, CSV, and JSON files as 'assets and data', and anything else that doesn't fit these categories as 'specialized'. Some files have already been classified, but are included for context. They need not be reclassified unless a classification is obviously wrong. 'None' or 'null' values, however, should be replaced with the correct role.\n{format_instructions}\nHere is the map of the project file structure:\n{input_str}",
    input_variables=["input_str"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    output_parser=parser
)


# Query a chatbot to determine the role that files play in the project
def classify_files(
            project_map_file: Path,
            project_files: list[ProjectFile],
            llm: ChatOpenAI,
            long_context_llm: ChatOpenAI
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
    project_map: FileClassificationList = query_llm(
                prompt=file_classification_prompt,
                input_str=input_str,
                llm=llm,
                long_context_llm=long_context_llm,
                parser=parser
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
