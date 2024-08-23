import gradio as gr
import modules.shared as shared

def on_ui_settings():
    section = ('LLM Prompt Artisan', 'LLM Prompt Artisan')
    shared.opts.add_option('anthropic_api_key', shared.OptionInfo('', 'Anthropic API Key', section=section))
    shared.opts.add_option('anthropic_cache_enabled', shared.OptionInfo(True, 'Enable Anthropic Prompt cache', gr.Checkbox, {}, section=section))
    shared.opts.add_option('openai_api_key', shared.OptionInfo('', 'OpenAI API Key', section=section))
    shared.opts.add_option('opt_temperature', shared.OptionInfo(1, 'temperature (default=1)', gr.Slider, {'minimum': 0, 'maximum': 1, 'step': 0.1}, section=section))
    shared.opts.add_option('max_retry', shared.OptionInfo(1, 'Number of automatic retries on generation errors (default=1)', gr.Slider, {'minimum': 0, 'maximum': 10, 'step': 1}, section=section))
    shared.opts.add_option('output_lang', shared.OptionInfo('JP', 'Language for generated titles and descriptions (default=JP)', gr.Dropdown, {'choices': ['JP', 'EN']}, section=section))
