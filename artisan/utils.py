import os
import json
import datetime
from modules.paths import data_path
from constants.constants import MODE_MAPPING, OUTPUT_DIR, FIXED_TAGS_FILE
import math

def save_log(log_data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(OUTPUT_DIR, f"generated_logs.jsonl")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
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
    
    # "Negative prompt:"の行を探す
    negative_prompt_index = next((i for i, line in enumerate(params_lines) if line.startswith("Negative prompt:")), -1)
    
    if negative_prompt_index != -1:
        # "Negative prompt:"より上の行を新しいプロンプトで置き換える
        params_lines[:negative_prompt_index] = [prompt_text]
    else:
        # "Negative prompt:"が見つからない場合は、最初の行を置き換える
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

def load_request_history(page=1, items_per_page=15):
    # folder_path = os.path.join(data_path, 'prompt_artisan_logs')
    file_path = os.path.join(OUTPUT_DIR, f"generated_logs.jsonl")
    
    if not os.path.exists(file_path):
        return "<p>No requests made yet.</p>", 0, 0

    with open(file_path, 'r', encoding='utf-8') as f:
        logs = [json.loads(line) for line in f]
    
    logs.reverse()  # 最新のログを先頭に

    total_items = len(logs)
    total_pages = math.ceil(total_items / items_per_page)
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    
    logs_page = logs[start_index:end_index]

    html = "<table><tr><th>Timestamp</th><th>Mode</th><th>Request</th><th>Generated Prompt</th><th>Title</th><th>Points</th></tr>"
    for log in logs_page:
        mode = MODE_MAPPING.get(log.get('mode', 0), "Unknown")
        request = truncate_string(log.get('prompt_request', 'Blank'))
        generated_prompt = truncate_string(log.get('response', {}).get('generated_prompt', ''), 120)
        title = truncate_string(log.get('response', {}).get('title', ''))
        points = truncate_string(log.get('response', {}).get('points', ''), 80)
        html += f"<tr><td>{log['timestamp']}</td><td>{mode}</td><td>{request}</td><td>{generated_prompt}</td><td>{title}</td><td>{points}</td></tr>"
    html += "</table>"
    
    return html, page, total_pages

def load_fixed_tags():
    print("Loading fixed tags...")
    if os.path.exists(FIXED_TAGS_FILE):
        with open(FIXED_TAGS_FILE, 'r') as f:
            tags = json.load(f)
            print(f"Loaded fixed tags: {tags}")
            return tags
    print("No fixed tags found")
    return {'prefix': '', 'suffix': ''}

def save_fixed_tags(prefix, suffix):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(FIXED_TAGS_FILE, 'w') as f:
        json.dump({'prefix': prefix, 'suffix': suffix}, f)