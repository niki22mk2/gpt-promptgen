import gradio as gr
import openai
import time, os, datetime, re

import modules.shared as shared
from scripts.conversational.message_history import MessageHistory
from scripts.template.prompt_template import (
    SYSTEM_PROMPTS,
    BASE_INSTRUCTIONS,
    CONVERSATIONAL_USER_PROMPTS
)

message_history = MessageHistory()

def on_ui_tabs():
    with gr.Blocks() as conversational_interface:
        with gr.Row(equal_height=True):
            with gr.Column(variant='panel'):                
                gr.Markdown(value="このモードでは、前のレスポンスを踏まえたリクエストが可能です。",style={"width": "100%", "overflow": "auto"})                    
                generated_prompt = gr.Textbox(
                    label="Generated Prompt",
                    interactive=False,
                    show_progress=True,
                    style={"width": "100%", "height": "100px", "overflow": "auto"}
                ).style(show_copy_button=True)
                supplementary_information = gr.Markdown(
                    label="Supplementary Information",
                    style={"width": "100%"}
                )
                gr.Markdown(value="***",style={"width": "100%", "overflow": "auto"})                    
                with gr.Row():
                    prompt_request = gr.Textbox(
                        label="Input request",
                        placeholder="Enter request",
                        value="",
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
            with gr.Column(variant='panel'):
                gr.Markdown(value="History (簡易)",style={"width": "100%", "overflow": "auto"})
                gr.Markdown(value="***",style={"width": "100%", "overflow": "auto"})                    
                history_display = gr.Markdown(
                    label="History",
                    style={"width": "100%", "height": "100%", "overflow": "auto"}
                )
        generate_prompt_button.click(
            fn=generate_prompt,
            inputs=[prompt_request],
            outputs=[generated_prompt, history_display,supplementary_information]
        )
        prompt_request.submit(
            fn=generate_prompt,
            inputs=[prompt_request],
            outputs=[generated_prompt, history_display,supplementary_information]
        )
        clear_button.click(
            fn=clear_history,
            inputs=[],
            outputs=[prompt_request, generated_prompt, history_display,supplementary_information]
        )

    return (conversational_interface, "Conversational (experimental)", "conversational_interface"),

def update_history_display():
    history_text = message_history.get_history_text(full=True)
    history_text = history_text.replace('\n', '<br>')
    return history_text

def clear_history():
    message_history.clear_history()
    return "", "", "", ""

def save_log_to_file(context, type):
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    folder_path = os.path.join(shared.cmd_opts.data_dir, 'promptgen_log', type)
    file_path = os.path.join(folder_path, timestamp + '.txt')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(file_path, 'a') as f:
        f.write(context)
        f.write("\n\n")

def process_prompt(prompt_request):
    openai.api_key = shared.opts.open_ai_key
    prompt_lang = "JP"
    prompt_lang_instructions = prompt_lang

    system_prompt = SYSTEM_PROMPTS[prompt_lang]

    history_text = message_history.get_history_text()
    user_prompt = BASE_INSTRUCTIONS[prompt_lang_instructions] + CONVERSATIONAL_USER_PROMPTS[prompt_lang].format(history=history_text, request=prompt_request)

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
            response_text = response_text.replace("You:", "Prompt:")

            prompt_match = re.search(r'Prompt:\s*(.+)', response_text)
            title_match = re.search(r'Title:\s*(.+)', response_text)
            points_match = re.search(r'Points:\s*(.+)', response_text, flags=re.DOTALL)

            if not title_match or not prompt_match:
                raise ValueError("Invalid response_text format:", response_text)

            prompt_text = prompt_match.group(1).strip()
            title = title_match.group(1).strip()
            points = points_match.group(1).strip()

            supplementary_info = f"### Title: {title}\n\nPoints: {points}"

            message_history.add_message(prompt_request, {"prompt": prompt_text, "title": title, "points": points})

            return prompt_text, supplementary_info

        except Exception as e:
            if attempt < max_retries - 1:
                print(f"An error occurred while generating the prompt. Retrying in {retry_interval} seconds... (Attempt {attempt + 1}/{max_retries})")
                print(f"Error details: {e}")
                time.sleep(retry_interval)
            else:
                print(f"Failed to generate the prompt after {max_retries} attempts. Please try again later.")
                return "", f'### <span style="color: red">Error: Failed to generate the prompt. Please retry Generate Prompt.</span> <br><br>{e}'

def generate_prompt(prompt_request):
    prompt_text, supplementary_info = process_prompt(prompt_request)
    history_text = update_history_display()
    return prompt_text, history_text, supplementary_info
