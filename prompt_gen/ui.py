import gradio as gr
from modules import infotext_utils, shared
from .core import generate_prompt, improve_prompt
from utilities.logs import update_request_history, load_request_history
from utilities.params import update_params_content
from utilities.fixed_tags import load_fixed_tags, save_fixed_tags
from constants.constants import MODE_NAME_MAPPING, VENDOR_MODELS
from .config import config

def create_ui():
    with gr.Blocks() as llm_prompt_gen_interface:
        with gr.Column(elem_classes="llm-prompt-gen-container"):
            with gr.Tab("Prompt Generation"):
                with gr.Row():
                    with gr.Column(scale=2):
                        prompt_request = gr.Textbox(
                            label="Prompt request",
                            placeholder="Enter request",
                            lines=2
                        )
                        with gr.Row():
                            mode = gr.Radio(
                                choices=list(MODE_NAME_MAPPING.values()),
                                label="Mode",
                                value="🖊️ Generate"
                            )
                        
                        image_model_type = gr.Radio(
                            choices=["SDXL", "FLUX"],
                            label="Image Model Type (SDXL: Danbooru tag prompts for Animagine XL, FLUX: Natural language prompts)",
                            value="SDXL"
                        )

                        content_type = gr.Radio(
                            choices=["NORMAL", "NSFW"],
                            label="Content Type (Account bans due to NSFW content generation are at your own risk)",
                            value="NORMAL"
                        )

                        with gr.Row():
                            vendor = gr.Dropdown(
                                choices=list(VENDOR_MODELS.keys()),
                                label="LLM Vendor",
                                value="Anthropic"
                            )
                            model = gr.Dropdown(
                                choices=VENDOR_MODELS["Anthropic"],
                                label="LLM Model",
                                value=VENDOR_MODELS["Anthropic"][0]
                            )

                        with gr.Row():
                            generate_prompt_button = gr.Button("Send", variant='primary')
                            clear_button = gr.Button("Clear", variant='secondary')
                        
                        with gr.Accordion("Optional Settings", open=False):
                            fixed_tags_state = gr.State(load_fixed_tags())
                            fixed_tags_prefix = gr.Textbox(
                                label="Fixed tags to prepend",
                                placeholder="Enter tags to add at the beginning of all prompts",
                                value=""
                            )
                            fixed_tags_suffix = gr.Textbox(
                                label="Fixed tags to append",
                                placeholder="Enter tags to add at the end of all prompts",
                                value=""
                            )

                            # 画像アップロード用のコンポーネントを追加
                            reference_image = gr.Image(
                                label="Reference Image (optional)",
                                type="pil"
                            )

                    with gr.Column(scale=3):
                        generated_prompt = gr.Textbox(
                            label="Generated Prompt",
                            interactive=False,
                            lines=5,
                            elem_id="generated-prompt"
                        )
                        supplementary_information = gr.Markdown(
                            label="Supplementary Information"
                        )
                        with gr.Row():
                            send_to_buttons = infotext_utils.create_buttons(["txt2img", "img2img"])
                            improve_button = gr.Button("Refine and Enhance", variant='primary')
                        
                        with gr.Accordion("Thinking Process", open=False):
                            thinking_information = gr.Markdown()

            with gr.Tab("Request History"):
                initial_history, initial_page, initial_total = load_request_history()
                with gr.Row():
                    request_history = gr.HTML(
                        value=initial_history,
                        elem_id="request-history-content"
                    )
                with gr.Row(elem_id="pagination-row"):
                    with gr.Column(scale=1):
                        prev_page = gr.Button("◀", elem_classes="pagination-button")
                    with gr.Column(scale=2):
                        page_info = gr.HTML(f"<div id='page-info'>Page {initial_page} of {initial_total}</div>")
                    with gr.Column(scale=1):
                        next_page = gr.Button("▶", elem_classes="pagination-button")
                
                # 非表示の要素としてページ情報を保持
                current_page = gr.Number(value=initial_page, visible=False)
                total_pages = gr.Number(value=initial_total, visible=False)

            full_info_textbox = gr.Textbox(visible=False)

            # イベントハンドラーの設定
            generate_prompt_button.click(
                fn=generate_prompt_wrapper,
                inputs=[prompt_request, mode, fixed_tags_prefix, fixed_tags_suffix, content_type, vendor, model, image_model_type, reference_image],
                outputs=[generated_prompt, supplementary_information, request_history, full_info_textbox, thinking_information, current_page, total_pages]
            )

            improve_button.click(
                fn=improve_prompt_wrapper,
                inputs=[generated_prompt, fixed_tags_prefix, fixed_tags_suffix, content_type, vendor, model, image_model_type],
                outputs=[generated_prompt, supplementary_information, thinking_information, full_info_textbox]
            )

            clear_button.click(
                fn=lambda: ["", "", "", "", ""],
                inputs=[],
                outputs=[prompt_request, generated_prompt, supplementary_information, request_history, thinking_information]
            )

            # 固定タグの保存と full_info_textbox の更新
            def update_fixed_tags_and_full_info(prefix, suffix, current_prompt):
                save_fixed_tags(prefix, suffix)
                return update_full_info(current_prompt, prefix, suffix)

            fixed_tags_prefix.change(
                fn=update_fixed_tags_and_full_info,
                inputs=[fixed_tags_prefix, fixed_tags_suffix, generated_prompt],
                outputs=[full_info_textbox]
            )
            fixed_tags_suffix.change(
                fn=update_fixed_tags_and_full_info,
                inputs=[fixed_tags_prefix, fixed_tags_suffix, generated_prompt],
                outputs=[full_info_textbox]
            )

            # Send to buttonsの設定
            for tabname, button in send_to_buttons.items():
                infotext_utils.register_paste_params_button(
                    infotext_utils.ParamBinding(
                        paste_button=button,
                        tabname=tabname,
                        source_text_component=full_info_textbox,
                        source_image_component=None
                    )
                )

            def update_history(page):
                history_html, current, total = load_request_history(page=page)
                return [history_html, current, total, gr.HTML.update(value=f"<div id='page-info'>Page {current} of {total}</div>")]

            prev_page.click(
                fn=lambda page: update_history(max(1, page - 1)),
                inputs=[current_page],
                outputs=[request_history, current_page, total_pages, page_info]
            )

            next_page.click(
                fn=lambda page, total: update_history(min(total, page + 1)),
                inputs=[current_page, total_pages],
                outputs=[request_history, current_page, total_pages, page_info]
            )
            
            # ベンダー選択が変更されたときにモデル選択を更新
            vendor.change(fn=update_model_choices, inputs=[vendor], outputs=[model])

        llm_prompt_gen_interface.load(
            fn=lambda x: (x['prefix'], x['suffix']),
            inputs=fixed_tags_state,
            outputs=[fixed_tags_prefix, fixed_tags_suffix]
        )
    
    
    return [(llm_prompt_gen_interface, "LLM Prompt Gen", "llm_prompt_gen_interface")]

def get_openrouter_models():
    """OpenRouterのモデルリストを取得します。設定画面で指定されたカスタムモデルも含みます。"""
    base_models = VENDOR_MODELS["OpenRouter"].copy()
    custom_models = config.openrouter_custom_models
    
    if custom_models:
        base_models.extend(custom_models)
    
    return base_models

def update_model_choices(vendor):
    """ベンダー選択に応じてモデル選択を更新する関数"""
    if vendor == "OpenRouter":
        models = get_openrouter_models()
    else:
        models = VENDOR_MODELS[vendor]
    
    return gr.Dropdown.update(choices=models, value=models[0])

def update_full_info(generated_prompt, fixed_tags_prefix, fixed_tags_suffix):
    if generated_prompt:
        full_prompt = (fixed_tags_prefix + ", " if fixed_tags_prefix else "") + generated_prompt + (", " + fixed_tags_suffix if fixed_tags_suffix else "")
        full_prompt = full_prompt.strip().strip(',')  # 先頭と末尾のカンマと空白を削除
        print(f"[Prompt-Gen] Update prompt for send to buttons")
        full_info_with_tags = update_params_content(full_prompt)
        # print(f"[Prompt-Gen] Full info with tags: {full_info_with_tags}")
        return full_info_with_tags
    return ""

def generate_prompt_wrapper(prompt_request, mode, fixed_tags_prefix, fixed_tags_suffix, content_type, vendor, model, image_model_type, reference_image):
    mode_number = list(MODE_NAME_MAPPING.values()).index(mode)
    prompt_text, title, points, thinking_text = generate_prompt(prompt_request, mode_number, content_type, vendor, model, image_model_type, reference_image)
    
    # 表示用の文字列を組み立て
    supplementary_info = f"### {title}\n{points}"
    
    # 固定タグを追加
    full_prompt = (fixed_tags_prefix + ", " if fixed_tags_prefix else "") + prompt_text + (", " + fixed_tags_suffix if fixed_tags_suffix else "")
    full_prompt = full_prompt.strip().strip(',') 
    full_info_with_tags = update_params_content(full_prompt)
    
    updated_history, current_page, total_pages = update_request_history(prompt_request, mode_number, {
        "title": title,
        "generated_prompt": prompt_text,
        "points": points
    })
    return prompt_text, supplementary_info, updated_history, full_info_with_tags, thinking_text, current_page, total_pages

def improve_prompt_wrapper(generated_prompt, fixed_tags_prefix, fixed_tags_suffix, content_type, vendor, model, image_model_type):
    prompt_text, title, points, thinking_text = improve_prompt(generated_prompt, content_type, vendor, model, image_model_type)
    supplementary_info = f"### {title}\n{points}"
    full_prompt = (fixed_tags_prefix + ", " if fixed_tags_prefix else "") + prompt_text + (", " + fixed_tags_suffix if fixed_tags_suffix else "")
    full_prompt = full_prompt.strip().strip(',')
    full_info_with_tags = update_params_content(full_prompt)
    return prompt_text, supplementary_info, thinking_text, full_info_with_tags
