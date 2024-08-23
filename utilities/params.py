import pathlib
from modules.paths import data_path

def get_params_content():
    filename = pathlib.Path(data_path, "params.txt")
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
    
    if (negative_prompt_index != -1):
        # "Negative prompt:"より上の行を新しいプロンプトで置き換える
        params_lines[:negative_prompt_index] = [prompt_text]
    else:
        # "Negative prompt:"が見つからない場合は、最初の行を置き換える
        params_lines[0] = prompt_text
    
    return '\n'.join(params_lines)