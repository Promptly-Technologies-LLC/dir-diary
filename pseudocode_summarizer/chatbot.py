import os
from dotenv import load_dotenv
from typing import Optional
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from openai.error import InvalidRequestError
from langchain.output_parsers import PydanticOutputParser
from langchain.callbacks import StdOutCallbackHandler
from pydantic import BaseModel


# Initialize OpenAI chatbot
def initialize_model(
            api_key: str = None,
            temperature: float = 0,
            model_name: str = "gpt-3.5-turbo",
            callbacks: Optional[list] = None
        ) -> ChatOpenAI:
    # If no API key is provided, load it from the .env file or environment
    if api_key is None:
        load_dotenv()
        api_key: str = os.getenv(key="OPENAI_API_KEY")

    # Create a chatbot instance using langchain
    llm: ChatOpenAI = ChatOpenAI(
        openai_api_key=api_key,
        model_name=model_name,
        max_tokens=2000,
        temperature=temperature,
        callbacks=callbacks
    )

    # Return the chatbot instance
    return llm


# Query a chatbot for structured output with pydantic validation
def query_llm(
            prompt: PromptTemplate,
            input_str: str,
            llm: ChatOpenAI,
            long_context_llm: ChatOpenAI,
            parser: Optional[PydanticOutputParser]) -> BaseModel:
    
    # Create a chatbot chain
    llm_chain: LLMChain = LLMChain(
        llm=llm,
        prompt=prompt,
        callbacks=[StdOutCallbackHandler()]
    )

    # Generate the output from the input
    try:
        output_str: str = llm_chain.run(input_str=input_str)
    except InvalidRequestError as e:
        # If we exceed context limit, check if long_context_llm is None
        if long_context_llm is None:
            # If long_context_llm is None, raise the error
            raise e
        else:
            # If long_context_llm is not None, warn and use long_context_llm
            print("Encountered error:\n" + e + "\nTrying again with long_context_fallback.")
            llm_chain.llm = long_context_llm
            output_str: str = llm_chain.run(input_str=input_str)
    
    # Parse the output
    if parser is None:
        # If no parser is provided, return the raw output
        return output_str
    else:
        # If a parser is provided, parse the output
        parsed_output: BaseModel = parser.parse(text=output_str)

        # Return the parsed output
        return parsed_output
