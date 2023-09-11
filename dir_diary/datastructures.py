from typing import Optional, Literal
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, Field
import json

# Define allowed summary types, roles, and models as sets
ALLOWED_SUMMARY_TYPES = {"tech stack", "pseudocode", "usage"}
ALLOWED_ROLES = {"source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", "specialized"}
ALLOWED_MODELS = {"gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", "gpt-4", "gpt-4-0314", "gpt-4-0613"}

# Generic validation function
def validate_value(value, allowed_set, var_name) -> None:
    if value not in allowed_set:
        raise ValueError(f"The `{var_name}` argument must be one of {allowed_set}")

# Function to validate multiple arguments
def validate_arguments(arguments) -> None:
    for arg in arguments:
        var_name = arg['var_name']
        allowed_set = arg['allowed_set']
        value = arg['value']
        if isinstance(value, list):
            for val in value:
                validate_value(value=val, allowed_set=allowed_set, var_name=var_name)
        else:
            validate_value(value=value, allowed_set=allowed_set, var_name=var_name)

# Data structure for project file metadata (use Literal rather than Enum
# because it plays nicer with LLM prompting and JSON serialization
class ProjectFile(BaseModel):
    path: Path
    modified: datetime
    role: Optional[Literal["source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", "specialized"]] = Field(
            default=None, description="role the file plays in the project"
        )

# Data structure for LLM project map response (use Literal rather than Enum
# because it plays nicer with LLM prompting and JSON serialization
class FileClassification(BaseModel):
    path: Path = Field(description="file path relative to the project root")
    role: Optional[Literal["source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", "specialized"]] = Field(
            default=None, description="role the file plays in the project"
        )

# Data structure for a list of FileClassifications
class FileClassificationList(BaseModel):
    files: list[FileClassification] = Field(
            description="List of file classifications"
        )

    # Method to convert a FileClassificationList to a JSON-formatted string
    def to_json(self) -> str:
        data_dict = self.model_dump(exclude_unset=True)

        # Convert Path objects to str
        for file in data_dict.get("files", []):
            file["path"] = str(object=file["path"])

        return json.dumps(obj=data_dict)

# Data structure to hold the generated module summary
class ModulePseudocode(BaseModel):
    path: Path
    modified: datetime
    content: str