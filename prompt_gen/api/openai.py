from openai import OpenAI
from ..config import config
from utilities.image_utils import process_reference_image
import base64

class OpenAIAPI:
    def __init__(self):
        self.client = OpenAI(api_key=config.openai_api_key)

    def generate_message(self, system_prompt, user_prompt, prefill="", model="gpt-4o-2024-08-06", reference_image=None):
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": []}
            ]

            # テキストコンテンツを追加
            messages[1]["content"].append({
                "type": "text",
                "text": user_prompt + prefill if prefill else user_prompt
            })

            # 参考画像が提供された場合、画像コンテンツを追加
            if reference_image:
                img_str = process_reference_image(reference_image)
                if img_str:
                    messages[1]["content"].append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_str}"
                        }
                    })

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=config.opt_temperature,
                max_tokens=4096
            )

            print(f"[Prompt-Gen] OpenAI API usage: {response.usage}")

            text = response.choices[0].message.content.strip()
            return prefill + text if prefill else text
        except Exception as e:
            raise Exception(f"Error generating message with OpenAI: {str(e)}")