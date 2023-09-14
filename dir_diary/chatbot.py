from .validators import validate_temperature
from typing import Optional, Union
from dotenv import load_dotenv
from os import getenv
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from openai.error import InvalidRequestError
from langchain.output_parsers import PydanticOutputParser
from langchain.callbacks import StdOutCallbackHandler, get_openai_callback
from pydantic import BaseModel


class LLMClient:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LLMClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gpt-3.5-turbo", long_context_fallback: Optional[str] = "gpt-3.5-turbo-16k", temperature: float = 0, total_cost: Optional[Union[float, int]] = 0) -> None:
        if LLMClient._initialized:
            return
        # If no API key is provided, load it from the .env file or environment
        if api_key is None:
            load_dotenv()
            self.api_key: str = getenv(key="OPENAI_API_KEY")
        else:
            self.api_key: str = api_key
        self.model_name: str = model_name
        self.long_context_fallback: str = long_context_fallback
        self.temperature: float = validate_temperature(temperature=temperature)
        if not total_cost:
            self.total_cost: Union[float, int] = 0
        else:
            self.total_cost: Union[float, int] = total_cost
        LLMClient._initialized = True


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
