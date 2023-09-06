from typing import Literal
from pathlib import Path

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.schema import AIMessage
from langchain.prompts.base import StringPromptValue
from pydantic import BaseModel, Field

from .chatbot import initialize_model

# Desired data structure for LLM output
class FileClassification(BaseModel):
    path: str = Field(description="file path relative to the project root")
    classification: Literal["include","ignore"] = Field(description="whether to include or ignore the file")

# Data structure for a list of FileClassifications
class FileClassificationList(BaseModel):
    files: list[FileClassification] = Field(description="List of file classifications")

# Parser for the LLM output
parser = PydanticOutputParser(pydantic_object=FileClassificationList)

# Prompt for determining which files to add to pseudocodeignore and which to summarize
file_classification_prompt = PromptTemplate(
    template="We have mapped the file structure of a project folder for an existing coding project. We want to generate a high-level pseudocode summary of the project, but first we need to decide which files to include and which to ignore. Based on the file names and folder structure, let's classify all module files as 'include', but 'ignore' any configuration, build, test, documentation, or asset files.\n{format_instructions}\nHere are the file paths to classify: {file_paths}\n",
    input_variables=["file_paths"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


# Query a chatbot to determine which new files to add to pseudocodeignore and which to summarize
def classify_new_files(new_files: list[str], api_key: str, model_name: str, temperature: float) -> tuple[list[Path], list[Path]]:
    # Initialize OpenAI chatbot
    llm: ChatOpenAI = initialize_model(api_key=api_key, temperature=temperature, model_name=model_name)
    
    # Generate a prompt from the template and the new_files input
    _input: StringPromptValue = file_classification_prompt.format_prompt(file_paths=", ".join(new_files))

    # Generate the output from the input
    output: AIMessage = llm(_input.to_messages())

    # Parse the output into a FileClassificationList with Pydantic
    parsed_output: FileClassificationList = parser.parse(text=output.content)
    
    # Filter the list of FileClassifications into two lists of file paths
    include_files: list = []
    ignore_files: list = []
    for file in parsed_output.files:
        if file.classification == "include":
            include_files.append(Path(file.path))
        elif file.classification == "ignore":
            ignore_files.append(Path(file.path))

    # Return the two lists of file paths
    return include_files, ignore_files