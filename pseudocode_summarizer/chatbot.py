import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from openai.error import InvalidRequestError
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel


# Initialize OpenAI chatbot
def initialize_model(
            api_key: str = None,
            temperature: float = 0,
            model_name: str = "gpt-3.5-turbo"
        ) -> ChatOpenAI:
    # If no API key is provided, load it from the .env file or environment
    if api_key is None:
        load_dotenv()
        api_key: str = os.getenv(key="OPENAI_API_KEY")
        print("Using API key from .env file")

    # Create a chatbot instance using langchain
    llm: ChatOpenAI = ChatOpenAI(
        openai_api_key=api_key,
        model_name=model_name,
        max_tokens=2000,
        temperature=temperature
    )

    # Return the chatbot instance
    return llm


# Query a chatbot for structured output with pydantic validation
def query_llm_for_structured_output(
            prompt: PromptTemplate,
            input_str: str,
            llm: ChatOpenAI,
            long_context_llm: ChatOpenAI,
            callbacks: list[BaseCallbackHandler],
            parser: PydanticOutputParser) -> BaseModel:
    # Create a chatbot chain
    llm_chain: LLMChain = LLMChain(
        llm=llm,
        prompt=prompt,
        callbacks=callbacks
    )

    # Generate the output from the input
    try:
        output_str: dict = llm_chain(input_str, callbacks=callbacks)
    except InvalidRequestError as e:
        # If we exceed context limit, check if long_context_llm is None
        if long_context_llm is None:
            # If long_context_llm is None, raise the error
            raise e
        else:
            # If long_context_llm is not None, warn and use long_context_llm
            print("Encountered error:\n" + e + "\nTrying again with long_context_fallback.")
            llm_chain.llm = long_context_llm
            output_str: str = llm_chain(input_str, callbacks=callbacks)
    
    # Parse the output
    parsed_output: BaseModel = parser.parse(text=output_str)

    # Return the output
    return parsed_output
