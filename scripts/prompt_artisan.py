from modules import script_callbacks
from artisan.ui import create_ui
from artisan.settings import on_ui_settings

script_callbacks.on_ui_settings(on_ui_settings)
script_callbacks.on_ui_tabs(create_ui)