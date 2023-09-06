import os
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv


# Initialize OpenAI chatbot
def initialize_model(api_key: str = None, temperature: float = 0, model_name = "gpt-3.5-turbo") -> ChatOpenAI:
    # If no API key is provided, load it from the .env file or environment
    if api_key is None:
        load_dotenv()
        api_key = os.getenv(key="OPENAI_API_KEY")
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
