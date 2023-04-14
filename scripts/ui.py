import gradio as gr

from modules import script_callbacks
import modules.shared as shared
from scripts.promptgen import promptgen
from scripts.conversational import conversational


def on_ui_tabs():

    with gr.Blocks() as main_block:
        with gr.Tab("GPT-PromptGen", elem_id="tab_basic"):
            promptgen.on_ui_tabs()

        with gr.Tab("Conversational (experimental)", elem_id="tab_conversational"):
            conversational.on_ui_tabs()

    return (main_block, "GPT-PromptGen", "gpt_prompt_interface"),


def on_ui_settings():
    section = ('GPT-PromptGen', "GPT-PromptGen")
    shared.opts.add_option("open_ai_key", shared.OptionInfo("", "Open AI API Key *Required", section=section))
    shared.opts.add_option("open_ai_model", shared.OptionInfo("gpt-3.5-turbo", "Model to be used (default=gpt-3.5-turbo)", gr.Dropdown, lambda: {"choices": ["gpt-3.5-turbo","gpt-3.5-turbo-0301","gpt-4","gpt-4-0314","gpt-4-32k","gpt-4-32k-0314"]}, section=section))
    shared.opts.add_option("opt_temperature", shared.OptionInfo(1, "Sampling temperature (default=1)", gr.Slider, {"minimum": 0, "maximum": 2, "step": 0.1}, section=section))
    shared.opts.add_option("max_retry", shared.OptionInfo(1, "Number of automatic retries on generation errors (default=1)", gr.Slider, {"minimum": 0, "maximum": 10, "step": 1}, section=section))
    shared.opts.add_option("prompt_lang", shared.OptionInfo(False, "Use the English Prompt (not recommended)", section=section))
    shared.opts.add_option("output_lang", shared.OptionInfo(False, "Output in English (not recommended)", section=section))
    shared.opts.add_option("save_request_log", shared.OptionInfo(True, "Save request logs to a file. ([webui root folder]/promptgen_log/request/)", section=section))
    shared.opts.add_option("save_response_log", shared.OptionInfo(True, "Save response logs to a file. ([webui root folder]/promptgen_log/response/)", section=section))

script_callbacks.on_ui_settings(on_ui_settings)
script_callbacks.on_ui_tabs(on_ui_tabs)

