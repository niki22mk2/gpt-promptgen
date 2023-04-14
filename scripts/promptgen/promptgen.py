import gradio as gr
import openai
import time,os,datetime,re

import modules.shared as shared
from modules import generation_parameters_copypaste as parameters_copypaste
from scripts.template.prompt_template import (
    SYSTEM_PROMPTS,
    BASE_INSTRUCTIONS,
    BASIC_USER_PROMPTS,
    IMPROVE_USER_PROMPTS,
    FILL_IN_THE_BLANKS_USER_PROMPTS,
    NAMING_USER_PROMPTS,
)

def on_ui_tabs():
    with gr.Blocks() as gpt_prompt_interface:
        with gr.Row(equal_height=True):
            with gr.Column(variant='panel'):
                with gr.Column(variant='panel'):
                    prompt_request = gr.Textbox(
                        label="Prompt request",
                        placeholder="Enter request",
                        value="",
                        style={"width": "100%"}
                    )
                    mode_radio = gr.Radio(
                        ["Prompt Generation", "Refine and Enhance","Fill-in-the-Blanks", "Title and Points Generation"],
                        label="Mode",
                        inline=True,
                        style={"width": "100%"}
                    )
                    with gr.Row():
                        generate_prompt_button = gr.Button(
                            elem_id="generate_prompt_button",
                            value="Send",
                            variant='primary',
                            style={"width": "50%"}
                        )
                        clear_button = gr.Button(
                            elem_id="clear_button",
                            value="Clear",
                            variant='secondary',
                            style={"width": "50%"}
                        )
                    gr.Markdown(value="Request History",style={"width": "100%", "overflow": "auto"})
                    request_history = gr.Markdown(
                        placeholder="No requests made yet.",
                        style={"width": "100%", "overflow": "auto"}
                    )

            with gr.Column(variant='panel'):
                generated_prompt = gr.Textbox(
                    label="Generated Prompt",
                    interactive=False,
                    show_progress=True,
                    style={"width": "100%", "height": "100px", "overflow": "auto"}
                ).style(show_copy_button=True)
                supplementary_information = gr.Markdown(
                    label="Supplementary Information",
                    placeholder="Enter supplementary information",
                    style={"width": "100%"}
                )
                with gr.Row():
                    parameters_copypaste.bind_buttons(
                        parameters_copypaste.create_buttons(
                            ["txt2img", "img2img"],
                        ),
                        None,
                        generated_prompt
                    ) 
                    improve_button = gr.Button(
                        elem_id="improve_button",
                        value="Refine and Enhance",
                        variant='primary',
                        style={"width": "30%"}
                    ) 
        generate_prompt_button.click(
            fn=generate_prompt,
            inputs=[prompt_request, request_history, mode_radio],
            outputs=[generated_prompt, supplementary_information, request_history]
        )

        improve_button.click(
            fn=improve_prompt,
            inputs=[generated_prompt],
            outputs=[generated_prompt, supplementary_information]
        )

        clear_button.click(
            fn=lambda: ["", "", "",""],
            inputs=[],
            outputs=[prompt_request, generated_prompt, supplementary_information,request_history]
        )

    return (gpt_prompt_interface, "GPT-PromptGen", "gpt_prompt_interface"),


def save_log_to_file(context, type):
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    folder_path = os.path.join(shared.cmd_opts.data_dir, 'promptgen_log', type)
    file_path = os.path.join(folder_path, timestamp + '.txt')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(file_path, 'a') as f:
        f.write(context)
        f.write("\n\n")

def process_prompt(prompt_request, user_prompt_type):
    openai.api_key = shared.opts.open_ai_key
    prompt_lang = "EN" if shared.opts.prompt_lang else "JP"
    prompt_lang_instructions = prompt_lang
    if shared.opts.output_lang:
        prompt_lang_instructions = "EN_ALL"

    system_prompt = SYSTEM_PROMPTS[prompt_lang]
    user_prompt = BASE_INSTRUCTIONS[prompt_lang_instructions] + user_prompt_type[prompt_lang].format(request=prompt_request)

    #print(user_prompt)

    max_retries = shared.opts.max_retry + 1
    retry_interval = 2

    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model=shared.opts.open_ai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=shared.opts.opt_temperature,
                timeout = 60
            )

            response_text = response.choices[0].message["content"].strip()
            response_text = re.sub(r'\n+', '\n', response_text)

            prompt_match = re.search(r'Prompt:\s*(.+)', response_text)
            title_match = re.search(r'Title:\s*(.+)', response_text)
            points_match = re.search(r'Points:\s*(.+)', response_text, flags=re.DOTALL)

            if not title_match or not prompt_match:
                raise ValueError("Invalid response_text format:", response_text)

            prompt_text = prompt_match.group(1).strip()
            title = title_match.group(1).strip()
            points = points_match.group(1).strip()

            supplementary_info = f"### Title: {title}\n\nPoints: {points}"
            if shared.opts.save_response_log:
                save_log_to_file(response_text, "response")

            if shared.opts.save_request_log and user_prompt_type == BASIC_USER_PROMPTS:
                save_log_to_file(prompt_request, "request")

            return prompt_text, supplementary_info

        except Exception as e:
            if attempt < max_retries - 1:
                print(f"An error occurred while generating the prompt. Retrying in {retry_interval} seconds... (Attempt {attempt + 1}/{max_retries})")
                print(f"Error details: {e}")
                time.sleep(retry_interval)
            else:
                print(f"Failed to generate the prompt after {max_retries} attempts. Please try again later.")
                return "", f'### <span style="color: red">Error: Failed to generate the prompt. Please retry Generate Prompt.</span> <br><br>{e}'


def generate_prompt(prompt_request, request_history, mode):
    prompt_template = BASIC_USER_PROMPTS

    if mode == "Prompt Generation":
        prompt_template = BASIC_USER_PROMPTS
    elif mode == "Fill-in-the-Blanks":
        prompt_template = FILL_IN_THE_BLANKS_USER_PROMPTS
    elif mode == "Title and Points Generation":
        prompt_template = NAMING_USER_PROMPTS
    elif mode == "Refine and Enhance":
        prompt_template = IMPROVE_USER_PROMPTS
    
    prompt_text, supplementary_info = process_prompt(prompt_request, prompt_template)
    
    list_tag = """
    <ul>
    <li> {content} </li>
    </ul>
    """
    # リクエスト履歴を更新
    if not (prompt_text == ""):
        new_history_entry = list_tag.format(content=prompt_request)
        updated_history = request_history + new_history_entry
    else:
        updated_history = request_history

    return prompt_text, supplementary_info, updated_history

def improve_prompt(prompt_request):
    prompt_text, supplementary_info = process_prompt(prompt_request, IMPROVE_USER_PROMPTS)

    return prompt_text, supplementary_info