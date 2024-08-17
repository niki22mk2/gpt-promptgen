from anthropic import Anthropic
from ..config import config

class AnthropicAPI:
    def __init__(self):
        self.client = Anthropic(api_key=config.anthropic_api_key)

    def generate_message(self, system_prompt, user_prompt, prefill=""):
        try:
            messages = [
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]

            # prefillがある場合、assistantメッセージを追加
            if prefill:
                messages.append({
                    "role": "assistant",
                    "content": prefill
                })

            response = self.client.beta.prompt_caching.messages.create(
                model=config.anthropic_model,
                max_tokens=4096,
                temperature=config.opt_temperature,
                system=[
                    {
                        "type": "text",
                        "text": system_prompt,
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                messages=messages
            )

            print(response.usage)

            # レスポンスにprefillを追加
            text = prefill + response.content[0].text.strip() if prefill else response.content[0].text.strip()
            return text
        except Exception as e:
            raise Exception(f"Error generating message: {str(e)}")