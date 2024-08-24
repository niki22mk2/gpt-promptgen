from modules import script_callbacks
from prompt_gen.ui import create_ui
from prompt_gen.settings import on_ui_settings

script_callbacks.on_ui_settings(on_ui_settings)
script_callbacks.on_ui_tabs(create_ui)