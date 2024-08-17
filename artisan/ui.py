from pathlib import Path
import gradio as gr
from modules import infotext_utils
from .core import generate_prompt, improve_prompt
from .utils import update_request_history
from constants.paths import EXTENSION_BASE_DIR

def create_ui():
    css_path = Path(EXTENSION_BASE_DIR, "static", "css", "style.css")
    js_path = Path(EXTENSION_BASE_DIR, "static", "js", "script.js")

    print("css_path:", css_path)
    print("js_path:", js_path)

    with gr.Blocks(css=css_path, js=js_path) as llm_prompt_artisan_interface:
        with gr.Column(elem_classes="llm-prompt-artisan-container"):
            gr.Markdown("# LLM Prompt Artisan")
            
            with gr.Row():
                with gr.Column(scale=2):
                    prompt_request = gr.Textbox(
                        label="Prompt request",
                        placeholder="Enter request",
                        lines=2
                    )
                    mode_radio = gr.Radio(
                        ["Prompt Generation", "Refine and Enhance", "Fill-in-the-Blanks", "Title and Points Generation"],
                        label="Mode",
                        interactive=True
                    )
                    with gr.Row():
                        generate_prompt_button = gr.Button("Send", variant='primary')
                        clear_button = gr.Button("Clear", variant='secondary')
                    
                    with gr.Accordion("Request History", open=False, elem_id="request-history-accordion"):
                        request_history = gr.HTML(
                            value="<ul></ul>",
                            elem_id="request-history-content"
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

            full_info_textbox = gr.Textbox(visible=False)

            # イベントハンドラーの設定
            generate_prompt_button.click(
                fn=generate_prompt_wrapper,
                inputs=[prompt_request, request_history, mode_radio],
                outputs=[generated_prompt, supplementary_information, request_history, full_info_textbox, thinking_information]
            )

            improve_button.click(
                fn=improve_prompt_wrapper,
                inputs=[generated_prompt],
                outputs=[generated_prompt, supplementary_information, thinking_information]
            )

            clear_button.click(
                fn=lambda: ["", "", "", "", ""],
                inputs=[],
                outputs=[prompt_request, generated_prompt, supplementary_information, request_history, thinking_information]
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

    return [(llm_prompt_artisan_interface, "LLM Prompt Artisan", "llm_prompt_artisan_interface")]

def generate_prompt_wrapper(prompt_request, request_history, mode):
    prompt_text, supplementary_info, full_info, thinking_text = generate_prompt(prompt_request, request_history, mode)
    updated_history = update_request_history(prompt_request, request_history)
    print(f"Debug - Old history: {request_history}")
    print(f"Debug - New history: {updated_history}")
    return prompt_text, supplementary_info, updated_history, full_info, thinking_text

def improve_prompt_wrapper(prompt_request):
    return improve_prompt(prompt_request)