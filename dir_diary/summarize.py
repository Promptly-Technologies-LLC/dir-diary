from .langchain_chatbot import LLMClient
from .classifier import classify_files
from .summarizer import summarize_file
from .file_handler import (read_summary_file, write_summary_file,
                           identify_new_and_modified_files,
                           remove_deleted_files_from_summaries,
                           ModuleSummary, ProjectFile)
from .mapper import (map_project_folder, remove_gitignored_files)
from .datastructures import ALLOWED_SUMMARY_TYPES, ALLOWED_ROLES, ALLOWED_MODELS, ALLOWED_FALLBACKS
from .validators import validate_literals, validate_paths
from pathlib import Path
from os import PathLike
from typing import Union, Literal


# Given a path to a project folder, summarize the folder in a markdown file
def summarize_project_folder(
            startpath: Union[str, PathLike] = ".",
            destination: Union[str, PathLike] = "docs",
            summary_types: Union[tuple, list[Literal[
                    "pseudocode", "usage", "tech stack"
                ]]] = ["pseudocode"],
            include: Union[tuple, list[Literal[
                    "source", "configuration", "build or deployment",
                    "documentation", "testing", "database", "utility scripts",
                    "assets or data", "specialized"
                ]]] = ["source", "utility scripts"],
            api_key: str = None,
            model_name: Literal[
                    "gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613",
                    "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", "gpt-4",
                    "gpt-4-0314", "gpt-4-0613"
                ] = "gpt-3.5-turbo",
            long_context_fallback: Literal[
                    'gpt-4', 'gpt-4-0314', 'gpt-4-0613', 'gpt-3.5-turbo-16k',
                    'gpt-3.5-turbo-16k-0613'
                ] = "gpt-3.5-turbo-16k",
            temperature: float = 0
        ) -> None:
    # Validate Literal argument values
    validate_literals(arguments=[
        {'var_name': 'summary_types', 'allowed_set': ALLOWED_SUMMARY_TYPES, 'value': summary_types},
        {'var_name': 'include', 'allowed_set': ALLOWED_ROLES, 'value': include},
        {'var_name': 'model_name', 'allowed_set': ALLOWED_MODELS, 'value': model_name},
        {'var_name': 'long_context_fallback', 'allowed_set': ALLOWED_FALLBACKS, 'value': long_context_fallback}
    ])

    # Validate Path arguments
    startpath, destination = validate_paths(startpath=startpath, destination=destination)

    # Initialize LLMClient to define configuration and track cost
    client = LLMClient(
            api_key=api_key,
            model_name=model_name,
            long_context_fallback=long_context_fallback,
            temperature=temperature,
            total_cost=0
        )

    # Map the project folder, outputting a list of ProjectFile objects
    project_files: list[ProjectFile] = map_project_folder(startpath=startpath)
    
    # Remove all project_files listed in .gitignore
    project_files: list[ProjectFile] = remove_gitignored_files(startpath=startpath, project_files=project_files)

    # Classify files by project role
    project_map_file: Path = Path(destination) / "project_map.json"
    project_files: list[ProjectFile] = classify_files(
            project_map_file=project_map_file,
            project_files=project_files
        )

    # Keep only project files with roles that are in the include list or tuple
    if isinstance(include, str):
        include = [include]
    project_files: list[ProjectFile] = [file for file in project_files if file.role in include]
    
    # For each summary type in both summary_types and ["pseudocode", "usage"], read or create the summary file
    summaries_to_generate: list[str] = [type for type in summary_types if type in ["pseudocode", "usage"]]
    for type in summaries_to_generate:
        file_path: Path = Path(destination) / (type + ".md")
    
        # Read or create the summary file and get ModuleSummary list
        summaries: list[ModuleSummary] = read_summary_file(summary_file=file_path)

        # Filter summaries to remove any files that have been deleted
        updated_summaries: list[ModuleSummary] = remove_deleted_files_from_summaries(summaries=summaries, files=project_files)

        # Output ProjectFile lists of new and modified files since last summary
        new_files, modified_files = identify_new_and_modified_files(
                summaries=summaries,
                project_files=project_files
            )
        files_to_summarize: list[ProjectFile] = new_files + modified_files

        # If there are no files_to_summarize and updated_summaries is identical to summaries, exit
        sorted_updated_summaries = sorted(updated_summaries, key=lambda x: (x.path, x.modified))
        sorted_summaries = sorted(summaries, key=lambda x: (x.path, x.modified))
        if not files_to_summarize and sorted_updated_summaries == sorted_summaries:
            return
        
        # For each file_to_summarize, query the chatbot for updated summary
        for file in files_to_summarize:
            generated_summaries: ModuleSummary = summarize_file(
                    file_to_summarize=file,
                    summary_type=type
                )
            # Drop any existing summaries for the file
            updated_summaries = [summary for summary in updated_summaries if summary.path != file.path]
            # Add the output to the updated_summaries
            updated_summaries.append(generated_summaries)
        
        # Write the updated summaries to the summary file
        write_summary_file(summaries=updated_summaries, summary_file=file_path)

    print("Total cost of workflow run: " + str(object=client.total_cost))

    return
