import json
import re
import time
from .config import config
from .utils import save_log, update_params_content
from constants.prompt_templates import (
    SYSTEM_PROMPTS,
    BASIC_USER_PROMPTS,
    IMPROVE_USER_PROMPTS,
    FILL_IN_THE_BLANKS_USER_PROMPTS,
    NAMING_USER_PROMPTS,
)
from .api.anthropic import AnthropicAPI

def process_prompt(prompt_request, user_prompt_type, mode_number):
    anthropic_api = AnthropicAPI()
    system_prompt = SYSTEM_PROMPTS[config.output_lang]
    user_prompt = user_prompt_type[config.output_lang].format(request=prompt_request)

    for attempt in range(config.max_retry + 1):
        try:
            response_text = anthropic_api.generate_message(system_prompt, user_prompt, prefill="<antThinking>")
            # print("Generated text:", response_text)
            thinking_text, output_json = parse_response(response_text)

            prompt_text = output_json['prompt'].strip()
            title = output_json['title']
            points = output_json['points']

            full_info = update_params_content(prompt_text)
            supplementary_info = f"### Title: {title}\n\nPoints: {points}"

            try:
                log_data = {
                    "prompt_request": prompt_request,
                    "mode": mode_number,
                    "response": {
                        "title": title,
                        "generated_prompt": prompt_text,
                        "points": points,
                    }
                }
                
                if config.save_log:
                    save_log(log_data)

            except Exception as e:
                print(f"An error occurred while saving the log: {e}")

            return prompt_text, supplementary_info, full_info, thinking_text

        except Exception as e:
            if attempt < config.max_retry:
                print(f"An error occurred while generating the prompt. Retrying in 2 seconds... (Attempt {attempt + 1}/{config.max_retry + 1})")
                print(f"Error details: {e}")
                time.sleep(2)
            else:
                print(f"Failed to generate the prompt after {config.max_retry + 1} attempts. Please try again later.")
                return "", f'### <span style="color: red">Error: Failed to generate the prompt. Please retry Generate Prompt.</span> <br><br>{e}', "", ""

def parse_response(response_text):
    thinking_match = re.search(r'<antThinking>(.*?)</antThinking>', response_text, re.DOTALL)
    thinking_text = thinking_match.group(1).strip() if thinking_match else ""

    output_match = re.search(r'<output>(.*?)</output>', response_text, re.DOTALL)
    if output_match:
        output_json = output_match.group(1).strip().replace('\\', '\\\\')
        return thinking_text, json.loads(output_json)
    else:
        raise ValueError("Output format not found in response")

def generate_prompt(prompt_request, mode_number):
    mode_mapping = {
        0: BASIC_USER_PROMPTS,
        1: IMPROVE_USER_PROMPTS,
        2: FILL_IN_THE_BLANKS_USER_PROMPTS,
        3: NAMING_USER_PROMPTS,
    }
    prompt_template = mode_mapping.get(mode_number, BASIC_USER_PROMPTS)

    return process_prompt(prompt_request, prompt_template, mode_number)

def improve_prompt(prompt_request):
    prompt_text, supplementary_info, _, thinking_text = process_prompt(prompt_request, IMPROVE_USER_PROMPTS, mode="🔄 Refine")
    return prompt_text, supplementary_info, thinking_text