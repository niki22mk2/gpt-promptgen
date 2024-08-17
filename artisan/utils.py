import os
import json
import datetime
from modules.paths import data_path
from .config import config
from constants.constants import MODE_MAPPING

def save_log(log_data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    folder_path = os.path.join(data_path, 'prompt_artisan_logs')
    file_path = os.path.join(folder_path, f"{datetime.datetime.now().strftime('%Y%m%d')}.jsonl")
    os.makedirs(folder_path, exist_ok=True)
    
    log_entry = {
        "timestamp": timestamp,
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

def update_request_history(prompt_request, mode_number, response_data):
    log_data = {
        "prompt_request": prompt_request,
        "mode": mode_number,
        "response": response_data
    }
    save_log(log_data)
    return load_request_history()

def truncate_string(s, max_length=50):
    return s if len(s) <= max_length else s[:max_length-3] + '...'

def load_request_history():
    folder_path = os.path.join(data_path, 'prompt_artisan_logs')
    file_path = os.path.join(folder_path, f"{datetime.datetime.now().strftime('%Y%m%d')}.jsonl")
    
    if not os.path.exists(file_path):
        return "<p>No requests made yet.</p>"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        logs = [json.loads(line) for line in f]
    
    logs.reverse()  # 最新のログを先頭に
    
    html = "<table><tr><th>Timestamp</th><th>Mode</th><th>Request</th><th>Generated Prompt</th><th>Title</th><th>Points</th></tr>"
    for log in logs[:50]:  # 最新の50件のみ表示
        mode = MODE_MAPPING.get(log.get('mode', 0), "Unknown")
        request = truncate_string(log.get('prompt_request', 'Blank'))
        generated_prompt = truncate_string(log.get('response', {}).get('generated_prompt', ''), 100)
        title = truncate_string(log.get('response', {}).get('title', ''))
        points = truncate_string(log.get('response', {}).get('points', ''))
        html += f"<tr><td>{log['timestamp']}</td><td>{mode}</td><td>{request}</td><td>{generated_prompt}</td><td>{title}</td><td>{points}</td></tr>"
    html += "</table>"
    
    return html