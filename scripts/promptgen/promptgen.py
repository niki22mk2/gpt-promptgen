import gradio as gr
import anthropic
import time,os,datetime,re
import json

import modules.shared as shared
from modules.paths import data_path
from modules import infotext_utils
from scripts.template.prompt_template import (
    SYSTEM_PROMPTS,
    BASE_INSTRUCTIONS,
    BASIC_USER_PROMPTS,
    IMPROVE_USER_PROMPTS,
    FILL_IN_THE_BLANKS_USER_PROMPTS,
    NAMING_USER_PROMPTS,
)

def on_ui_tabs():
    with gr.Blocks() as llm_prompt_artisan_interface:
        with gr.Row(equal_height=True):
            with gr.Column(variant='panel'):
                with gr.Column(variant='panel'):
                    prompt_request = gr.Textbox(
                        label="Prompt request",
                        placeholder="Enter request",
                        value=""
                    )
                    mode_radio = gr.Radio(
                        ["Prompt Generation", "Refine and Enhance","Fill-in-the-Blanks", "Title and Points Generation"],
                        label="Mode",
                        interactive=True
                    )
                    with gr.Row():
                        generate_prompt_button = gr.Button(
                            elem_id="generate_prompt_button",
                            value="Send",
                            variant='primary'
                        )
                        clear_button = gr.Button(
                            elem_id="clear_button",
                            value="Clear",
                            variant='secondary'
                        )
                    gr.Markdown("Request History")
                    request_history = gr.Markdown()

            # 非表示のTextboxを追加して完全な生成情報を保持
            full_info_textbox = gr.Textbox(visible=False)

            with gr.Column(variant='panel'):
                generated_prompt = gr.Textbox(
                    label="Generated Prompt",
                    interactive=False,
                    lines=4
                )
                supplementary_information = gr.Markdown(
                    label="Supplementary Information"
                )
                with gr.Row():
                    send_to_buttons = infotext_utils.create_buttons(["txt2img", "img2img"])
                    improve_button = gr.Button(
                        elem_id="improve_button",
                        value="Refine and Enhance",
                        variant='primary'
                    )
                thinking_information = gr.Markdown(  # 新しく追加
                    label="Thinking Process"
                )
        
        # register_paste_params_buttonの呼び出しを修正
        for tabname, button in send_to_buttons.items():
            infotext_utils.register_paste_params_button(
                infotext_utils.ParamBinding(
                    paste_button=button,
                    tabname=tabname,
                    source_text_component=full_info_textbox,  # 非表示のTextboxを使用
                    source_image_component=None
                )
            )

        generate_prompt_button.click(
            fn=generate_prompt,
            inputs=[prompt_request, request_history, mode_radio],
            outputs=[generated_prompt, supplementary_information, request_history, full_info_textbox, thinking_information]  # thinking_informationを追加
        )

        improve_button.click(
            fn=improve_prompt,
            inputs=[generated_prompt],
            outputs=[generated_prompt, supplementary_information, thinking_information]  # thinking_informationを追加
        )

        clear_button.click(
            fn=lambda: ["", "", "", "", ""],  # 空の文字列を1つ追加
            inputs=[],
            outputs=[prompt_request, generated_prompt, supplementary_information, request_history, thinking_information]  # thinking_informationを追加
        )

    return [(llm_prompt_artisan_interface, "LLM Prompt Artisan", "llm_prompt_artisan_interface")]

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
    client = anthropic.Anthropic(api_key=shared.opts.anthropic_api_key)
    prompt_lang = "EN" if shared.opts.prompt_lang else "JP"
    prompt_lang_instructions = prompt_lang
    if shared.opts.output_lang:
        prompt_lang_instructions = "EN_ALL"

    system_prompt = SYSTEM_PROMPTS[prompt_lang] + BASE_INSTRUCTIONS[prompt_lang_instructions]
    user_prompt =  user_prompt_type[prompt_lang].format(request=prompt_request)

    max_retries = shared.opts.max_retry + 1
    retry_interval = 2

    for attempt in range(max_retries):
        try:
            response = client.beta.prompt_caching.messages.create(
                model=shared.opts.anthropic_model,
                max_tokens=1024,
                temperature=shared.opts.opt_temperature,
                system=[
                    {
                        "type": "text",
                        "text": system_prompt,
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )

            response_text = response.content[0].text.strip()

            try:
                # Thinking部分を抽出
                thinking_match = re.search(r'<antThinking>(.*?)</antThinking>', response_text, re.DOTALL)
                thinking_text = thinking_match.group(1).strip() if thinking_match else ""

                # XMLタグ内のJSON形式の出力を抽出
                output_match = re.search(r'<output>(.*?)</output>', response_text, re.DOTALL)
                if output_match:
                    output_json = output_match.group(1).strip()
                    # バックスラッシュをエスケープ
                    output_json = output_json.replace('\\', '\\\\')
                    response_json = json.loads(output_json)
                else:
                    raise ValueError("Output format not found in response")

                prompt_text = response_json['prompt'].strip()
                title = response_json['title']
                points = response_json['points']

                # params.txtの内容を読み込む
                filename = os.path.join(data_path, "params.txt")
                try:
                    with open(filename, "r", encoding="utf8") as file:
                        params_content = file.read()
                except OSError:
                    params_content = "temp prompt\nNegative prompt:"

                # 1行目をgenerated_promptで置き換える
                params_lines = params_content.split('\n')
                params_lines[0] = prompt_text
                full_info = '\n'.join(params_lines)

                supplementary_info = f"### Title: {title}\n\nPoints: {points}"

                if shared.opts.save_response_log:
                    save_log_to_file(response_text, "response")

                if shared.opts.save_request_log and user_prompt_type == BASIC_USER_PROMPTS:
                    save_log_to_file(prompt_request, "request")

                return prompt_text, supplementary_info, full_info, thinking_text

            except (json.JSONDecodeError, ValueError) as e:
                raise ValueError(f"Error parsing response: {e}\nResponse text: {response_text}")

        except Exception as e:
            if attempt < max_retries - 1:
                print(f"An error occurred while generating the prompt. Retrying in {retry_interval} seconds... (Attempt {attempt + 1}/{max_retries})")
                print(f"Error details: {e}")
                time.sleep(retry_interval)
            else:
                print(f"Failed to generate the prompt after {max_retries} attempts. Please try again later.")
                return "", f'### <span style="color: red">Error: Failed to generate the prompt. Please retry Generate Prompt.</span> <br><br>{e}', "", ""

list_tag = """
<ul>
<li> {content} </li>
</ul>"""

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
    
    prompt_text, supplementary_info, full_info, thinking_text = process_prompt(prompt_request, prompt_template)

    # リクエスト履歴を更新
    if prompt_text:
        new_history_entry = list_tag.format(content=prompt_request)
        updated_history = request_history + new_history_entry
    else:
        updated_history = request_history

    return prompt_text, supplementary_info, updated_history, full_info, thinking_text 

def improve_prompt(prompt_request):
    prompt_text, supplementary_info, thinking_text = process_prompt(prompt_request, IMPROVE_USER_PROMPTS)

    return prompt_text, supplementary_info, thinking_text