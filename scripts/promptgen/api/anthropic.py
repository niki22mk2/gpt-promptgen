from anthropic import AsyncAnthropic
from ..config import config

class AnthropicAPI:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=config.anthropic_api_key)

    async def generate_message(self, system_prompt, user_prompt):
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