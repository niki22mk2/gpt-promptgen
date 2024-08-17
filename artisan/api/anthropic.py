from anthropic import AsyncAnthropic
from ..config import config
import asyncio

class AnthropicAPI:
    _instance = None
    _lock = asyncio.Lock()

    @classmethod
    async def get_instance(cls):
        async with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
                await cls._instance.initialize()
            return cls._instance

    def __init__(self):
        self.client = None

    async def initialize(self):
        self.client = AsyncAnthropic(api_key=config.anthropic_api_key)

    async def generate_message(self, system_prompt, user_prompt):
        if not self.client:
            await self.initialize()
        try:
            response = await self.client.beta.prompt_caching.messages.create(
                model=config.anthropic_model,
                max_tokens=1024,
                temperature=config.opt_temperature,
                system=[
                    {
                        "type": "text",
                        "text": system_prompt,
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            raise Exception(f"Error generating message: {str(e)}")

    async def cleanup(self):
        if self.client and hasattr(self.client, 'close'):
            try:
                await self.client.close()
            except Exception as e:
                print(f"Error during AnthropicAPI cleanup: {str(e)}")
        self.client = None

    @classmethod
    async def close(cls):
        if cls._instance:
            await cls._instance.cleanup()
            cls._instance = None