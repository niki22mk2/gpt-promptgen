import os
import datetime
from modules.paths import data_path
from .config import config

def save_log_to_file(context, type):
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    folder_path = os.path.join(data_path, 'promptgen_log', type)
    file_path = os.path.join(folder_path, f"{timestamp}.txt")
    os.makedirs(folder_path, exist_ok=True)
    with open(file_path, 'a') as f:
        f.write(context)
        f.write("\n\n")

def get_params_content():
    filename = os.path.join(data_path, "params.txt")
    try:
        with open(filename, "r", encoding="utf8") as file:
            return file.read()
    except OSError:
        return "temp prompt\nNegative prompt:"

def update_params_content(prompt_text):
    params_content = get_params_content()
    params_lines = params_content.split('\n')
    params_lines[0] = prompt_text
    return '\n'.join(params_lines)

list_tag = """
<ul>
<li> {content} </li>
</ul>"""

def update_request_history(prompt_request, request_history):
    if prompt_request:
        new_history_entry = list_tag.format(content=prompt_request)
        return request_history + new_history_entry
    return request_history