import json
import re
import random
import time
from .config import config
from utilities.prompts import get_template
from .api.anthropic import AnthropicAPI
from .api.openai import OpenAIAPI
from constants.constants import MODE_PROMPT_NAME_MAPPING

def get_system_prompt(content_type, image_model_type):
    prompt_key = f"{config.output_lang}_{image_model_type}_{content_type}"
    try:
        system_prompt = get_template('SYSTEM_PROMPTS', prompt_key)
        print(f"[Prompt-Gen] Using System Prompt: {prompt_key}")
        return system_prompt
    except KeyError:
        print(f"[Prompt-Gen] Warning: System prompt for '{prompt_key}' not found. Using default JP_SDXL_NORMAL.")
        return get_template('SYSTEM_PROMPTS', 'JP_SDXL_NORMAL')

def process_prompt(prompt_request, user_prompt_type, content_type, vendor, model, image_model_type="SDXL", reference_image=None):
    print(f"[Prompt-Gen] Selected User Prompt Type: {user_prompt_type}")
    user_prompt = get_template(user_prompt_type, config.output_lang).format(
        request=prompt_request, 
        seed=random.randint(1, 1000000)
    )
    
    system_prompt = get_system_prompt(content_type, image_model_type)

    api = AnthropicAPI() if vendor == "Anthropic" else OpenAIAPI()

    for attempt in range(config.max_retry + 1):
        try:
            response_text = api.generate_message(system_prompt, user_prompt, prefill="<antThinking>", model=model, reference_image=reference_image)
            thinking_text, output_json = parse_response(response_text)

            prompt_text = output_json['prompt'].strip()
            title = output_json.get('title', '')
            points = output_json.get('points', '')

            if not title:
                print('[Prompt-Gen] titleが取得できませんでした')
                print(f"[Prompt-Gen]\n{output_json}")
                title = '取得に失敗しました'
            if not points:
                print('[Prompt-Gen] pointsが取得できませんでした')
                print(f"[Prompt-Gen]\n{output_json}")
                points = '取得に失敗しました'

            return prompt_text, title, points, thinking_text

        except Exception as e:
            if attempt < config.max_retry:
                print(f"[Prompt-Gen] An error occurred while generating the prompt. Retrying in 2 seconds... (Attempt {attempt + 1}/{config.max_retry + 1})")
                print(f"[Prompt-Gen] Error details: {e}")
                time.sleep(2)
            else:
                print(f"[Prompt-Gen] Failed to generate the prompt after {config.max_retry + 1} attempts. Please try again later.")
                return "", "", "", f'### <span style="color: red">Error: Failed to generate the prompt. Please retry Generate Prompt.</span> <br><br>{e}'

def parse_response(response_text):
    thinking_match = re.search(r'<antThinking>(.*?)</antThinking>', response_text, re.DOTALL)
    thinking_text = thinking_match.group(1).strip() if thinking_match else ""

    output_match = re.search(r'<output>(.*?)</output>', response_text, re.DOTALL)
    if output_match:
        output_json = output_match.group(1).strip().replace('\\', '\\\\')
        return thinking_text, json.loads(output_json)
    else:
        raise ValueError("Output format not found in response")

def generate_prompt(prompt_request, mode_number, content_type, vendor, model, image_model_type, reference_image=None):
    user_prompt_type = MODE_PROMPT_NAME_MAPPING.get(mode_number, "BASIC_USER_PROMPTS")

    return process_prompt(prompt_request, user_prompt_type, content_type, vendor, model, image_model_type, reference_image)

def improve_prompt(prompt_request, content_type, vendor, model, image_model_type):
    return generate_prompt(prompt_request, 1, content_type, vendor, model, image_model_type)  # 1 is the mode number for "Refine"