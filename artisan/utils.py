import os
import json
import datetime
from modules.paths import data_path
from .config import config

def save_structured_log(log_data, log_type):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    folder_path = os.path.join(data_path, 'prompt_artisan_logs', log_type)
    file_path = os.path.join(folder_path, f"{datetime.datetime.now().strftime('%Y%m%d')}.jsonl")
    os.makedirs(folder_path, exist_ok=True)
    
    log_entry = {
        "timestamp": timestamp,
        "type": log_type,
        **log_data
    }
    
    with open(file_path, 'a', encoding='utf-8') as f:
        json.dump(log_entry, f, ensure_ascii=False)
        f.write('\n')

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

def update_request_history(prompt_request, request_history):
    content = prompt_request if prompt_request else "Blank Request"
    new_history_entry = f'<li>{content}</li>'
    
    if not request_history or request_history == "No requests made yet.":
        return f'<ul>{new_history_entry}</ul>'
    else:
        # 既存のリストの最後に新しいエントリーを追加
        return request_history[:-5] + new_history_entry + '</ul>'