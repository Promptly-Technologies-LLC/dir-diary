from .file_handler import ModulePseudocode, ProjectFile
from .chatbot import query_llm_for_structured_output
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# Data structure for LLM classification of project file roles
class GeneratedPseudocode(BaseModel):
    pseudocode: str = Field(description="abbreviated pseudocode summary of the code module")

# Parser for the LLM output
parser = PydanticOutputParser(pydantic_object=GeneratedPseudocode)

# Prompt to generate a pseudocode summary of a code module
summarization_prompt: PromptTemplate = PromptTemplate(
    template="Generate an abbreviated natural-language pseudocode summary of the following code. Make sure to include function, class, and argument names so a reader can understand the execution context and usage. Well-formatted pseudocode will separate object and function blocks with a blank line and will use hierarchical ordered and unordered lists to show execution sequence and logical relationships.\n{format_instructions}\nHere is the code to summarize:\n{input}",
    input_variables=["input"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    output_parser=parser
)


# Query a chatbot to generate a pseudocode summary of a module file
def summarize_file(
            file_to_summarize: ProjectFile,
            llm: ChatOpenAI,
            long_context_llm: str,
            callbacks: list[BaseCallbackHandler]
        ) -> ModulePseudocode:
    # Read the file
    with open(file=file_to_summarize.path, mode='r') as f:
        input_str: str = f.read()

    # Query the chatbot for a pseudocode summary and parse the output
    generated_pseudocode: GeneratedPseudocode = query_llm_for_structured_output(
                prompt=summarization_prompt,
                input_str=input_str,
                llm=llm,
                long_context_llm=long_context_llm,
                callbacks=callbacks,
                parser=parser
            )

    # Create a ModulePseudocode object from the output
    module_pseudocode: ModulePseudocode = ModulePseudocode(
            path=file_to_summarize.path,
            modified=file_to_summarize.modified,
            content=generated_pseudocode.pseudocode
        )
    
    # Return the generated pseudocode
    return module_pseudocode
