from .datastructures import FileClassificationList
from .client import LLMClient
from typing import Optional, Literal
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from openai.error import InvalidRequestError
from langchain.output_parsers import PydanticOutputParser
from langchain.callbacks import StdOutCallbackHandler, get_openai_callback
from pydantic import BaseModel


# Initialize OpenAI chatbot
def initialize_model(long: bool = False) -> ChatOpenAI:
    # Initialize LLMClient to get config and track cost
    client = LLMClient()
    
    # Set model_name based on config + `long` argument
    model_name = client.model_name if long else client.long_context_fallback
    
    # Set max_tokens based on model_name
    if "32k" in model_name:
        max_tokens = 16000
    elif "16k" in model_name:
        max_tokens = 8000
    elif "gpt-4" in model_name:
        max_tokens = 4000
    else:
        max_tokens = 2000
    
    # Initialize the chatbot using langchain
    llm: ChatOpenAI = ChatOpenAI(
        openai_api_key=client.api_key,
        model_name=model_name,
        max_tokens=max_tokens,
        temperature=client.temperature
    )

    # Return the chatbot instance
    return llm


# Query a chatbot for pydantic-validated structured or unstructured output
def query_llm(
            prompt: PromptTemplate,
            input_str: str,
            parser: Optional[PydanticOutputParser]) -> BaseModel:
    
    # Initialize the client
    client = LLMClient()

    # Initialize the chatbot
    llm: ChatOpenAI = initialize_model(long=False)

    # Create a chatbot chain
    llm_chain: LLMChain = LLMChain(
        llm=llm,
        prompt=prompt
    )

    # Generate the output from the input
    with get_openai_callback() as cb:
        try:
            output_str: str = llm_chain.run(input_str=input_str, callback=[StdOutCallbackHandler()])
        except InvalidRequestError as e:
            # If we exceed context limit, check if long_context_fallback is None
            if client.long_context_fallback is None:
                # If long_context_fallback is None, raise the error
                raise e
            else:
                # If long_context_fallback is not None, warn and use long_context_fallback
                print("Encountered error:\n" + e + "\nTrying again with long_context_fallback.")
                llm_chain.llm = client.long_context_fallback
                output_str: str = llm_chain.run(input_str=input_str, callback=[StdOutCallbackHandler()])
        client.total_cost += cb.total_cost
    
    # Parse the output
    if parser is None:
        # If no parser is provided, return the raw output
        return output_str
    else:
        # If a parser is provided, parse the output
        parsed_output: BaseModel = parser.parse(text=output_str)

        # Return the parsed output
        return parsed_output


# Parser for the LLM output
parser = PydanticOutputParser(pydantic_object=FileClassificationList)

# Prompt template for determining the roles that files play in the project
file_classification_prompt: PromptTemplate = PromptTemplate(
    template="We have mapped the file structure of a project folder for an existing coding project. Based solely on the file structure, let's attempt to classify them by the role they play in the project. We will label code modules, entry points, and endpoints as 'source'; config files, environment files, and dependency files as 'configuration'; build files, Docker files, and CI/CD files as 'build or deployment'; READMEs, CHANGELOGs, pseudocodes, project maps, licenses, and docs as 'documentation'; unit tests as 'testing'; migration, schema, and seed files as 'database', utility and action scripts as 'utility scripts', static assets like images, CSS, CSV, and JSON files as 'assets and data', and anything else that doesn't fit these categories (e.g., compiled distribution files) as 'specialized'. Some files may already be classified and included for context. They need not be reclassified unless a classification is obviously wrong. 'None' or 'null' values, however, should be replaced with the correct role.\n{format_instructions}\nHere is the map of the project file structure:\n{input_str}",
    input_variables=["input_str"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    output_parser=parser
)

def classify_with_langchain(input_str: str) -> FileClassificationList:
    # Query the LLM to update the project map
    project_map: FileClassificationList = query_llm(
                prompt=file_classification_prompt,
                input_str=input_str,
                parser=parser
            )

    # Return the project map
    return project_map


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

def summarize_with_langchain(input_str: str, summary_type: Literal["pseudocode", "usage"]) -> str:
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
    
    return generated_summary
