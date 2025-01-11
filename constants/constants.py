from pathlib import Path
from modules import scripts
from modules.paths import data_path

# インポート時に basedir を取得し保存
EXTENSION_BASE_DIR = Path(scripts.basedir())

OUTPUT_DIR = Path(data_path, 'llm_prompt_gen')

# 固定タグの設定ファイルのパス
FIXED_TAGS_FILE = Path(OUTPUT_DIR, 'fixed_tags.json')

MODE_NAME_MAPPING = {
    0: "🖊️ Generate",
    1: "🔄 Refine",
    2: "🧩 Fill Blanks",
    3: "📝 Title & Points"
}

MODE_PROMPT_NAME_MAPPING = {
    0: "BASIC_USER_PROMPTS",
    1: "IMPROVE_USER_PROMPTS",
    2: "FILL_IN_THE_BLANKS_USER_PROMPTS",
    3: "NAMING_USER_PROMPTS",
}

VENDOR_MODELS = {
    "Anthropic": ["claude-3-5-sonnet-20241022"],
    "OpenAI": ["chatgpt-4o-latest", "gpt-4o"],
    "Google": ["gemini-2.0-flash-exp"],
    "DeepSeek": ["deepseek-chat"],
    "OpenRouter": ["x-ai/grok-2-1212", "x-ai/grok-2-vision-1212", "amazon/nova-pro-v1"],
}