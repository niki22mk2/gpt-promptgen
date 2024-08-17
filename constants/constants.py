from pathlib import Path
from modules import scripts
from modules.paths import data_path

# インポート時に basedir を取得し保存
EXTENSION_BASE_DIR = Path(scripts.basedir())

OUTPUT_DIR = Path(data_path, 'prompt_artisan')

# 固定タグの設定ファイルのパス
FIXED_TAGS_FILE = Path(OUTPUT_DIR, 'fixed_tags.json')

MODE_MAPPING = {
    0: "🖊️ Generate",
    1: "🔄 Refine",
    2: "🧩 Fill Blanks",
    3: "📝 Title & Points"
}