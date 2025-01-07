from .anthropic import AnthropicAPI
from .openai import OpenAIAPI
from .google import GoogleAPI
from .openrouter import OpenRouterAPI
from .deepseek import DeepSeekAPI

class APIFactory:
    @staticmethod
    def get_api(vendor):
        if vendor == "Anthropic":
            return AnthropicAPI()
        elif vendor == "OpenAI":
            return OpenAIAPI()
        elif vendor == "Google":
            return GoogleAPI()
        elif vendor == "OpenRouter":
            return OpenRouterAPI()
        elif vendor == "DeepSeek":
            return DeepSeekAPI()
        else:
            raise ValueError(f"Unsupported vendor: {vendor}")