from .chatbot import initialize_model
from .classifier import classify_files
from .summarizer import summarize_file
from .file_handler import (read_pseudocode_file, write_pseudocode_file,
                           identify_new_and_modified_files,
                           remove_deleted_files_from_pseudocode,
                           ModulePseudocode, ProjectFile)
from .mapper import (map_project_folder, remove_gitignored_files)
from .datastructures import ALLOWED_ROLES, ALLOWED_MODELS, validate_arguments
from pathlib import Path
from os import PathLike
from typing import Union, Literal
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import OpenAICallbackHandler


# Given a path to a project folder, summarize the folder in pseudocode.md
def summarize_project_folder(
            startpath: Union[str, PathLike] = ".",
            pseudocode_file: Union[str, PathLike] = "docs/pseudocode.md",
            project_map_file: Union[str, PathLike] = "docs/project_map.json",
            include: list[Literal[
                    "source", "configuration", "build or deployment",
                    "documentation", "testing", "database", "utility scripts",
                    "assets or data", "specialized"
                ]] = ["source", "utility scripts"],
            api_key: str = None,
            model_name: Literal[
                    'gpt-3.5-turbo', 'gpt-3.5-turbo-0301', 'gpt-3.5-turbo-0613',
                    'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-16k-0613', 'gpt-4',
                    'gpt-4-0314', 'gpt-4-0613'
                ] = "gpt-3.5-turbo",
            long_context_fallback: Literal[
                    'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-16k-0613'
                ] = "gpt-3.5-turbo-16k",
            temperature: float = 0
        ) -> None:
    # Validate 'include', 'model_name', and 'long_context_fallback' values
    validate_arguments(arguments=[
        {'var_name': 'include', 'allowed_set': ALLOWED_ROLES, 'value': include},
        {'var_name': 'model_name', 'allowed_set': ALLOWED_MODELS, 'value': model_name},
        {'var_name': 'long_context_fallback', 'allowed_set': ALLOWED_MODELS, 'value': long_context_fallback}
    ])

    # Get relative file paths by prepending startpath
    pseudocode_file: Path = Path(startpath) / pseudocode_file
    project_map_file: Path = Path(startpath) / project_map_file
    
    # Map the project folder, outputting a list of ProjectFile objects
    project_files: list[ProjectFile] = map_project_folder(startpath=startpath)
    
    # Remove all project_files listed in .gitignore
    project_files: list[ProjectFile] = remove_gitignored_files(startpath=startpath, project_files=project_files)

    # Initialize OpenAI chatbot
    cost_tracker: OpenAICallbackHandler = OpenAICallbackHandler()
    llm: ChatOpenAI = initialize_model(api_key=api_key, temperature=temperature, model_name=model_name, callbacks=[cost_tracker])

    # If long_context_fallback is not None, initialize a second chatbot
    if long_context_fallback is not None:
        long_context_llm: ChatOpenAI = initialize_model(api_key=api_key, temperature=temperature, model_name=long_context_fallback, callbacks=[cost_tracker])
    else:
        long_context_llm = None

    # Classify files by project role
    project_files: list[ProjectFile] = classify_files(
            project_map_file=project_map_file,
            project_files=project_files,
            llm=llm,
            long_context_llm=long_context_llm
        )

    # Keep only project files with roles that are in the include list
    project_files: list[ProjectFile] = [file for file in project_files if file.role in include]
    
    # Read or create the pseudocode file and get ModulePseudocode list
    pseudocode: list[ModulePseudocode] = read_pseudocode_file(pseudocode_file=pseudocode_file)

    # Filter pseudocode summary to remove any files that have been deleted
    updated_pseudocode: list[ModulePseudocode] = remove_deleted_files_from_pseudocode(pseudocode=pseudocode, files=project_files)

    # Output ProjectFile lists of new and modified files since last summary
    new_files, modified_files = identify_new_and_modified_files(
            pseudocode=pseudocode,
            project_files=project_files
        )
    files_to_summarize: list[ProjectFile] = new_files + modified_files

    # If there are no files_to_summarize and updated_pseudocode is identical to pseudocode, exit
    sorted_updated_pseudocode = sorted(updated_pseudocode, key=lambda x: (x.path, x.modified))
    sorted_pseudocode = sorted(pseudocode, key=lambda x: (x.path, x.modified))
    if not files_to_summarize and sorted_updated_pseudocode == sorted_pseudocode:
        return
    
    # For each file_to_summarize, query the chatbot for an updated_pseudocode summary
    for file in files_to_summarize:
        generated_pseudocode: ModulePseudocode = summarize_file(
                file_to_summarize=file,
                llm=llm,
                long_context_llm=long_context_llm
            )
        # Drop any existing pseudocode for the file
        updated_pseudocode = [pseudocode for pseudocode in updated_pseudocode if pseudocode.path != file.path]
        # Add the output to the updated_pseudocode
        updated_pseudocode.append(generated_pseudocode)
    
    # Write the updated pseudocode to the pseudocode file
    write_pseudocode_file(pseudocode=updated_pseudocode, pseudocode_file=pseudocode_file)

    print("Total cost of workflow run: " + str(object=cost_tracker.total_cost))

    return
