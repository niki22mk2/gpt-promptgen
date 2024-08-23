import pathlib
import json
import datetime
import math
from constants.constants import MODE_NAME_MAPPING, OUTPUT_DIR

def save_log(log_data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = pathlib.Path(OUTPUT_DIR, f"generated_logs.jsonl")
    output_dir = pathlib.Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    log_entry = {
        "timestamp": timestamp,
        **log_data
    }
    
    with open(file_path, 'a', encoding='utf-8') as f:
        json.dump(log_entry, f, ensure_ascii=False)
        f.write('\n')

def load_request_history(page=1, items_per_page=15):
    file_path = pathlib.Path(OUTPUT_DIR, f"generated_logs.jsonl")
    
    if not file_path.exists():
        return "<p>No requests made yet.</p>", 0, 0

    with open(file_path, 'r', encoding='utf-8') as f:
        logs = [json.loads(line) for line in f]
    
    logs.reverse()  # 最新のログを先頭に

    total_items = len(logs)
    total_pages = math.ceil(total_items / items_per_page)
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    
    logs_page = logs[start_index:end_index]

    html = "<table id='history-table'><tr><th>Timestamp</th><th>Mode</th><th>Request</th><th>Generated Prompt</th><th>Title</th><th>Points</th><th>Action</th></tr>"
    for index, log in enumerate(logs_page):
        row_id = f"history-row-{start_index + index}"
        mode = MODE_NAME_MAPPING.get(log.get('mode', 0), "Unknown")
        request = log.get('prompt_request', 'Blank')
        generated_prompt = log.get('response', {}).get('generated_prompt', '')
        title = log.get('response', {}).get('title', '')
        points = log.get('response', {}).get('points', '')
        html += f"<tr id='{row_id}'><td>{log['timestamp']}</td><td>{mode}</td><td class='truncate'>{request}</td><td class='truncate'>{generated_prompt}</td><td class='truncate'>{title}</td><td class='truncate'>{points}</td><td><button class='view-details-btn' data-row-id='{row_id}'>View</button></td></tr>"
    html += "</table>"

    # 非表示の詳細情報を含むdivを追加
    html += "<div id='history-details' style='display:none;'></div>"
    
    return html, page, total_pages

def update_request_history(prompt_request, mode_number, response_data):
    log_data = {
        "prompt_request": prompt_request,
        "mode": mode_number,
        "response": response_data
    }
    save_log(log_data)
    return load_request_history()