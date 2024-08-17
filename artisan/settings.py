import gradio as gr
import modules.shared as shared

def on_ui_settings():
    section = ('LLM Prompt Artisan', 'LLM Prompt Artisan')
    shared.opts.add_option('anthropic_api_key', shared.OptionInfo('', 'Anthropic API Key *Required', section=section))
    shared.opts.add_option('anthropic_model', shared.OptionInfo('claude-3-5-sonnet-20240620', 'Model to be used (default=claude-3-5-sonnet-20240620)', gr.Dropdown, {'choices': ['claude-3-5-sonnet-20240620', 'claude-3-opus-20240229',  'claude-3-haiku-20240307']}, section=section))
    shared.opts.add_option('opt_temperature', shared.OptionInfo(1, 'Sampling temperature (default=1)', gr.Slider, {'minimum': 0, 'maximum': 2, 'step': 0.1}, section=section))
    shared.opts.add_option('max_retry', shared.OptionInfo(1, 'Number of automatic retries on generation errors (default=1)', gr.Slider, {'minimum': 0, 'maximum': 10, 'step': 1}, section=section))
    shared.opts.add_option('output_lang', shared.OptionInfo('JP', 'Language for generated titles and descriptions (default=JP)', gr.Dropdown, {'choices': ['JP', 'EN']}, section=section))
    shared.opts.add_option('save_log', shared.OptionInfo(True, 'Save logs to a file. ([webui root folder]/prompt_artisan_logs/)', section=section))