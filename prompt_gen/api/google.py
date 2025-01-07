import google.generativeai as genai
from ..config import config
from utilities.image_utils import process_reference_image
import base64
from PIL import Image
from io import BytesIO
import os

class GoogleAPI:
    def __init__(self):
        genai.configure(api_key=config.google_api_key)

    def upload_image_to_gemini(self, image_data, mime_type):
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        buffer = BytesIO()
        image.save(buffer, format=mime_type.split('/')[1])
        file_path = 'temp_image.' + mime_type.split('/')[1]
        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())
        uploaded_file = genai.upload_file(file_path, mime_type=mime_type)
        os.remove(file_path)
        return uploaded_file

    def generate_message(self, system_prompt, user_prompt, prefill="", model="gemini-1.5-pro-002", reference_image=None):
        try:
            generation_config = {
                "temperature": config.opt_temperature,
                "max_output_tokens": 4096,
            }

            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]

            model_instance = genai.GenerativeModel(
                model_name=model,
                generation_config=generation_config,
                safety_settings=safety_settings,
                system_instruction=[system_prompt]
            )

            chat_session = model_instance.start_chat()

            # prefillをuser_promptの末尾に追加
            full_user_prompt = user_prompt + prefill

            imagenames = []
            images = []
            if reference_image:
                img_str = process_reference_image(reference_image)
                if img_str:
                    uploaded_image = self.upload_image_to_gemini(img_str, "image/png")
                    imagenames.append(uploaded_image.name)
                    images.append(uploaded_image)

            response = chat_session.send_message(
                content=[full_user_prompt, *images],
                safety_settings=safety_settings
            )

            text = response.text.strip()

            for name in imagenames:
                genai.delete_file(name)

            print(f"[Prompt-Gen] Google API usage: {response.prompt_feedback}")
            return text

        except Exception as e:
            raise Exception(f"Error generating message with Google: {str(e)}")