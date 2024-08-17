import json
import re
import time
from .config import config
from .utils import save_log_to_file, update_params_content
from constants.prompt_templates import (
    SYSTEM_PROMPTS,
    BASE_INSTRUCTIONS,
    BASIC_USER_PROMPTS,
    IMPROVE_USER_PROMPTS,
    FILL_IN_THE_BLANKS_USER_PROMPTS,
    NAMING_USER_PROMPTS,
)
from .api.anthropic import AnthropicAPI

async def process_prompt(prompt_request, user_prompt_type):
    anthropic_api = await AnthropicAPI.get_instance()
    system_prompt = SYSTEM_PROMPTS[config.prompt_lang] + BASE_INSTRUCTIONS[config.output_lang]
    user_prompt = user_prompt_type[config.prompt_lang].format(request=prompt_request)

    for attempt in range(config.max_retry + 1):
        try:
            response_text = await anthropic_api.generate_message(system_prompt, user_prompt)
            thinking_text, output_json = parse_response(response_text)

            prompt_text = output_json['prompt'].strip()
            title = output_json['title']
            points = output_json['points']

            full_info = update_params_content(prompt_text)
            supplementary_info = f"### Title: {title}\n\nPoints: {points}"

            if config.save_response_log:
                save_log_to_file(response_text, "response")

            if config.save_request_log and user_prompt_type == BASIC_USER_PROMPTS:
                save_log_to_file(prompt_request, "request")

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

async def generate_prompt(prompt_request, request_history, mode):
    prompt_template = {
        "Prompt Generation": BASIC_USER_PROMPTS,
        "Fill-in-the-Blanks": FILL_IN_THE_BLANKS_USER_PROMPTS,
        "Title and Points Generation": NAMING_USER_PROMPTS,
        "Refine and Enhance": IMPROVE_USER_PROMPTS,
    }.get(mode, BASIC_USER_PROMPTS)

    return await process_prompt(prompt_request, prompt_template)

async def improve_prompt(prompt_request):
    prompt_text, supplementary_info, _, thinking_text = await process_prompt(prompt_request, IMPROVE_USER_PROMPTS)
    return prompt_text, supplementary_info, thinking_text