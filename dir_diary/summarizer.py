from .file_handler import ModulePseudocode, ProjectFile
from .chatbot import query_llm
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

# Prompt to generate a pseudocode summary of a code module
summarization_prompt: PromptTemplate = PromptTemplate(
    template="Generate an abbreviated natural-language pseudocode summary of the following code. Make sure to include function, class, and argument names so a reader can understand the execution context and usage. Well-formatted pseudocode will separate object and function blocks with a blank line and will use hierarchical ordered and unordered lists to show execution sequence and logical relationships.\nHere is the code to summarize:\n{input_str}",
    input_variables=["input_str"]
)


# Query a chatbot to generate a pseudocode summary of a module file
def summarize_file(
            file_to_summarize: ProjectFile,
            llm: ChatOpenAI,
            long_context_llm: str
        ) -> ModulePseudocode:
    # Read the file
    with open(file=file_to_summarize.path, mode='r') as f:
        input_str: str = f.read()

    # Query the chatbot for a pseudocode summary and parse the output
    generated_pseudocode: str = query_llm(
                prompt=summarization_prompt,
                input_str=input_str,
                llm=llm,
                long_context_llm=long_context_llm,
                parser=None
            )

    # Create a ModulePseudocode object from the output
    module_pseudocode: ModulePseudocode = ModulePseudocode(
            path=file_to_summarize.path,
            modified=file_to_summarize.modified,
            content=generated_pseudocode
        )
    
    # Return the generated pseudocode
    return module_pseudocode
