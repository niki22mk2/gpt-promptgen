import gradio as gr

from modules import script_callbacks
import modules.shared as shared
from scripts.promptgen import promptgen

def on_ui_tabs():
    with gr.Blocks() as main_block:
        with gr.Tab("LLM Prompt Artisan", elem_id="tab_basic"):
            promptgen.on_ui_tabs()

    return (main_block, "LLM Prompt Artisan", "llm_prompt_artisan_interface"),


def on_ui_settings():
    section = ('LLM Prompt Artisan', "LLM Prompt Artisan")
    shared.opts.add_option("anthropic_api_key", shared.OptionInfo("", "Anthropic API Key *Required", section=section))
    shared.opts.add_option("anthropic_model", shared.OptionInfo("claude-3-5-sonnet-20240620", "Model to be used (default=claude-3-5-sonnet-20240620)", gr.Dropdown, {"choices": ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229",  "claude-3-haiku-20240307"]}, section=section))
    shared.opts.add_option("opt_temperature", shared.OptionInfo(1, "Sampling temperature (default=1)", gr.Slider, {"minimum": 0, "maximum": 2, "step": 0.1}, section=section))
    shared.opts.add_option("max_retry", shared.OptionInfo(1, "Number of automatic retries on generation errors (default=1)", gr.Slider, {"minimum": 0, "maximum": 10, "step": 1}, section=section))
    shared.opts.add_option("prompt_lang", shared.OptionInfo(False, "Use the English Prompt (not recommended)", section=section))
    shared.opts.add_option("output_lang", shared.OptionInfo(False, "Output in English (not recommended)", section=section))
    shared.opts.add_option("save_request_log", shared.OptionInfo(True, "Save request logs to a file. ([webui root folder]/promptgen_log/request/)", section=section))
    shared.opts.add_option("save_response_log", shared.OptionInfo(True, "Save response logs to a file. ([webui root folder]/promptgen_log/response/)", section=section))

script_callbacks.on_ui_settings(on_ui_settings)
script_callbacks.on_ui_tabs(on_ui_tabs)