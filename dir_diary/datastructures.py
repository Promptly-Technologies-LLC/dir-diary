from typing import Optional, Literal
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, Field
import json

# Define allowed summary types, roles, and models as sets
ALLOWED_SUMMARY_TYPES = {"pseudocode", "usage", "tech stack"}
ALLOWED_ROLES = {"source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", "specialized"}
ALLOWED_MODELS = {"gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", "gpt-4", "gpt-4-0314", "gpt-4-0613"}
ALLOWED_FALLBACKS = {'gpt-4', 'gpt-4-0314', 'gpt-4-0613', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-16k-0613'}

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
class ModuleSummary(BaseModel):
    path: Path
    modified: datetime
    content: str
