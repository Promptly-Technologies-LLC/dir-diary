from .validators import validate_temperature, validate_api_key
from dotenv import load_dotenv
from os import getenv
from typing import Optional, Union

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
            api_key: str = getenv(key="OPENAI_API_KEY")
        self.api_key: str = validate_api_key(api_key=api_key)
        self.model_name: str = model_name
        self.long_context_fallback: str = long_context_fallback
        self.temperature: float = validate_temperature(temperature=temperature)
        if not total_cost:
            self.total_cost: Union[float, int] = 0
        else:
            self.total_cost: Union[float, int] = total_cost
        LLMClient._initialized = True
