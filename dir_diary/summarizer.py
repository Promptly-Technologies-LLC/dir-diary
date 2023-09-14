from typing import Literal
from .file_handler import ModuleSummary, ProjectFile
from .chatbot import query_llm
from langchain import PromptTemplate

# Prompt to generate a pseudocode summary of a code module
pseudocode_prompt: PromptTemplate = PromptTemplate(
    template="Generate an abbreviated natural-language pseudocode summary of the following code. Make sure to include function, class, and argument names and to indicate where objects are imported from so a reader can understand the execution context and usage. Well-formatted pseudocode will separate object and function blocks with a blank line and will use hierarchical ordered and unordered lists to show execution sequence and logical relationships.\nHere is the code to summarize:\n{input_str}",
    input_variables=["input_str"]
)

# Prompt to generate a usage summary of a code module
usage_prompt: PromptTemplate = PromptTemplate(
    template="Generate natural-language instructions on how to use the following code. Describe what the code is doing, how to create instances or invoke methods of defined objects, and how to invoke functions. As much as possible, infer what data types are expected by function arguments and class methods, as well as what data types are returned. When usage cannot be inferred for types and classes imported from outside this module, flag the uncertainties and indicate where they are imported from. Well-formatted usage summaries will separate instructions for different objects and functions with a blank line.\nHere is the code to summarize:\n{input_str}",
    input_variables=["input_str"]
)


# Query a chatbot to generate a pseudocode summary of a module file
def summarize_file(
            file_to_summarize: ProjectFile,
            summary_type: Literal["pseudocode", "usage"]
        ) -> ModuleSummary:
    # Read the file
    with open(file=file_to_summarize.path, mode='r') as f:
        input_str: str = f.read()

    # Determine the prompt to use
    if summary_type == "pseudocode":
        prompt: PromptTemplate = pseudocode_prompt
    elif summary_type == "usage":
        prompt: PromptTemplate = usage_prompt

    # Query the chatbot for a summary and parse the output
    generated_summary: str = query_llm(
                prompt=prompt,
                input_str=input_str,
                parser=None
            )

    # Create a ModuleSummary object from the output
    module_summary: ModuleSummary = ModuleSummary(
            path=file_to_summarize.path,
            modified=file_to_summarize.modified,
            content=generated_summary
        )
    
    # Return the generated summary
    return module_summary
