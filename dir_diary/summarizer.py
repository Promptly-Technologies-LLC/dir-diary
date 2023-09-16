from typing import Literal
from .file_handler import ModuleSummary, ProjectFile
from .openai_chatbot import summarize_with_openai


# Query a chatbot to generate a pseudocode summary of a module file
def summarize_file(
            file_to_summarize: ProjectFile,
            summary_type: Literal["pseudocode", "usage"]
        ) -> ModuleSummary:
    # Read the file
    with open(file=file_to_summarize.path, mode='r') as f:
        input_str: str = f.read()

    # Query the chatbot for a summary and parse the output
    generated_summary: str = summarize_with_openai(
                input_str=input_str,
                summary_type=summary_type
            )
    
    # If any line in the summary starts with a hashtag, remove it and wrap
    # the line with double asterisks instead
    generated_summary: str = replace_hashtags(text=generated_summary)

    # Create a ModuleSummary object from the output
    module_summary: ModuleSummary = ModuleSummary(
            path=file_to_summarize.path,
            modified=file_to_summarize.modified,
            content=generated_summary
        )
    
    # Return the generated summary
    return module_summary


# If any line in the summary starts with a hashtag, remove it and wrap the
# line with double asterisks instead because hashtags will break file parsing
def replace_hashtags(text: str) -> str:
    cleaned_text: str = "\n".join(
        [
            f"**{line[1:].lstrip()}**" if line.startswith("#") else line
            for line in text.split(sep="\n")
        ]
    )
    return cleaned_text
