from anthropic import Anthropic
from ..config import config
from utilities.image_utils import process_reference_image

class AnthropicAPI:
    def __init__(self):
        self.client = Anthropic(api_key=config.anthropic_api_key, timeout=30.0)

    def generate_message(self, system_prompt, user_prompt, prefill="", model="claude-3-5-sonnet-20241022", reference_image=None):
        try:
            messages = [
                {
                    "role": "user",
                    "content": []
                }
            ]

            # テキストコンテンツを追加
            messages[0]["content"].append({
                "type": "text",
                "text": user_prompt
            })

            # 参考画像が提供された場合、画像コンテンツを追加
            if reference_image:
                img_str = process_reference_image(reference_image)
                if img_str:
                    messages[0]["content"].append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": img_str
                        }
                    })

            if prefill:
                messages.append({
                    "role": "assistant",
                    "content": prefill
                })

            system = [
                {
                    "type": "text",
                    "text": system_prompt,
                }
            ]

            # キャッシュが有効の場合、cache_controlを追加
            if config.anthropic_cache_enabled:
                system[0]["cache_control"] = {"type": "ephemeral"}
                print(f"[Prompt-Gen] Anthropic Prompt cache enabled")

            response = self.client.beta.prompt_caching.messages.create(
                model=model,
                max_tokens=4096,
                temperature=config.opt_temperature,
                system=system,
                messages=messages
            )

            print(f"[Prompt-Gen] Anthropic API usage: {response.usage}")

            text = prefill + response.content[0].text.strip() if prefill else response.content[0].text.strip()
            return text
        except Exception as e:
            raise Exception(f"Error generating message with Anthropic: {str(e)}")