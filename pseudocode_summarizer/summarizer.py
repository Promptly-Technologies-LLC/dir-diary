from .file_handler import ModulePseudocode, ProjectFile
from typing import Literal
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI

# Prompt to generate a pseudocode summary of a code module
summarize_template: Literal = "Generate a pseudocode summary of the following code. Make sure to provide names for objects and dependencies so a reader can understand execution context and usage.\n{input}?"


# Query a chatbot to generate a pseudocode summary of a module file
def summarize_file(file_to_summarize: ProjectFile, llm: ChatOpenAI) -> ModulePseudocode:
    # Read the file
    with open(file=file_to_summarize.path, mode='r') as f:
        input: str = f.read()

    # Create a chatbot chain
    llm_chain: LLMChain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(template=summarize_template)
    )

    # Generate the output from the input
    output: dict = llm_chain(input)
    
    # Create a ModulePseudocode object from the output
    generated_pseudocode: ModulePseudocode = ModulePseudocode(
            path=file_to_summarize.path,
            modified=file_to_summarize.modified,
            content=output['text']
        )
    
    # Return the generated pseudocode
    return generated_pseudocode
