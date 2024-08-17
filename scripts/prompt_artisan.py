import gradio as gr
from modules import script_callbacks
import modules.shared as shared
from artisan.ui import create_ui
import atexit
import asyncio
from artisan.api.anthropic import AnthropicAPI

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
script_callbacks.on_ui_tabs(create_ui)

def cleanup_anthropic_api():
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(AnthropicAPI.close())
    else:
        loop.run_until_complete(AnthropicAPI.close())

atexit.register(cleanup_anthropic_api)