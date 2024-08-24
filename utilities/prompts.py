import toml
import pathlib
import re
from constants.constants import EXTENSION_BASE_DIR

def load_templates():
    templates_dir = pathlib.Path(EXTENSION_BASE_DIR, 'templates')
    all_templates = {}

    # templatesフォルダ内のすべてのTOMLファイルを再帰的に読み込む
    for toml_path in templates_dir.rglob('*.toml'):
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
            
            # パースしたTOMLを統合
            all_templates.update(unescape_quotes(parsed_toml))
        except FileNotFoundError:
            print(f"Error: {toml_path} file not found.")
            raise
        except toml.TomlDecodeError as e:
            print(f"Error: Invalid TOML format in {toml_path}: {e}")
            raise

    return all_templates

def get_template(template_type, prompt_key='JP_SDXL_NORMAL'):
    templates = load_templates()
    return templates[template_type][prompt_key]