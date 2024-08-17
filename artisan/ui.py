import gradio as gr
from modules import infotext_utils
from .core import generate_prompt, improve_prompt
from .utils import update_request_history, load_request_history
from constants.constants import MODE_MAPPING

def create_ui():
    with gr.Blocks() as llm_prompt_artisan_interface:
        with gr.Column(elem_classes="llm-prompt-artisan-container"):
            gr.Markdown("# LLM Prompt Artisan")
            
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
                                choices=list(MODE_MAPPING.values()),
                                label="Mode",
                                value="🖊️ Generate"
                            )
                        with gr.Row():
                            generate_prompt_button = gr.Button("Send", variant='primary')
                            clear_button = gr.Button("Clear", variant='secondary')

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
                with gr.Row():
                    request_history = gr.HTML(
                        value=load_request_history()[0],
                        elem_id="request-history-content"
                    )
                with gr.Row():
                    prev_page = gr.Button("Previous Page")
                    current_page = gr.Number(value=1, label="Current Page", interactive=False)
                    total_pages = gr.Number(value=1, label="Total Pages", interactive=False)
                    next_page = gr.Button("Next Page")

            full_info_textbox = gr.Textbox(visible=False)

            # イベントハンドラーの設定
            generate_prompt_button.click(
                fn=generate_prompt_wrapper,
                inputs=[prompt_request, mode],
                outputs=[generated_prompt, supplementary_information, request_history, full_info_textbox, thinking_information, current_page, total_pages]
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

            def update_history(page):
                history_html, current, total = load_request_history(page=page)
                return history_html, current, total

            prev_page.click(
                fn=lambda page: update_history(max(1, page - 1)),
                inputs=[current_page],
                outputs=[request_history, current_page, total_pages]
            )

            next_page.click(
                fn=lambda page, total: update_history(min(total, page + 1)),
                inputs=[current_page, total_pages],
                outputs=[request_history, current_page, total_pages]
            )

    return [(llm_prompt_artisan_interface, "LLM Prompt Artisan", "llm_prompt_artisan_interface")]

def generate_prompt_wrapper(prompt_request, mode):
    mode_number = list(MODE_MAPPING.values()).index(mode)
    prompt_text, supplementary_info, full_info, thinking_text = generate_prompt(prompt_request, mode_number)
    updated_history, current_page, total_pages = update_request_history(prompt_request, mode_number, {
        "generated_prompt": prompt_text,
        "title": supplementary_info.split("\n")[0].replace("### Title: ", ""),
        "points": "\n".join(supplementary_info.split("\n")[2:])
    })
    return prompt_text, supplementary_info, updated_history, full_info, thinking_text, current_page, total_pages

def improve_prompt_wrapper(prompt_request):
    return improve_prompt(prompt_request)