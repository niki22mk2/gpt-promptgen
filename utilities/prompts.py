import toml
import pathlib
import re
import json
from constants.constants import EXTENSION_BASE_DIR

def load_templates():
    toml_path = pathlib.Path(EXTENSION_BASE_DIR, 'constants', 'prompt_templates.toml')

    try:
        with open(toml_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # マルチラインストリング内のダブルクオーテーションをエスケープ
        content = re.sub(r'(\'\'\'[\s\S]*?\'\'\')', lambda m: m.group(1).replace('"', '\\"'), content)
        
        # TOMLをパース
        parsed_toml = toml.loads(content)
        
        # 再帰的に文字列内のエスケープされたダブルクオーテーションを元に戻す
        def unescape_quotes(obj):
            if isinstance(obj, str):
                return obj.replace('\\"', '"')
            elif isinstance(obj, dict):
                return {k: unescape_quotes(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [unescape_quotes(item) for item in obj]
            else:
                return obj
        
        return unescape_quotes(parsed_toml)
    except FileNotFoundError:
        print("Error: prompt_templates.toml file not found.")
        raise
    except toml.TomlDecodeError as e:
        print(f"Error: Invalid TOML format in prompt_templates.toml: {e}")
        raise

def get_template(template_type, lang='JP'):
    templates = load_templates()
    return templates[template_type][lang]