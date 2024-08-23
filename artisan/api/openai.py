from openai import OpenAI
from ..config import config

class OpenAIAPI:
    def __init__(self):
        self.client = OpenAI(api_key=config.openai_api_key)

    def generate_message(self, system_prompt, user_prompt, prefill="", model="gpt-4o-2024-08-06"):
        try:
            # print(f"system_prompt:\n{system_prompt}")
            # print(f"user_prompt:\n{user_prompt}")
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt + prefill if prefill else user_prompt}
            ]

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=config.opt_temperature,
                max_tokens=4096
            )

            print(f"[Prompt-Artisan] OpenAI API usage: {response.usage}")

            text = prefill + response.choices[0].message.content.strip() if prefill else response.choices[0].message.content.strip()
            return text
        except Exception as e:
            # print(f"response:\n{response}")
            raise Exception(f"Error generating message with OpenAI: {str(e)}")