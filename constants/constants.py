from pathlib import Path
from modules import scripts

# インポート時に basedir を取得し保存
EXTENSION_BASE_DIR = Path(scripts.basedir())

MODE_MAPPING = {
    0: "🖊️ Generate",
    1: "🔄 Refine",
    2: "🧩 Fill Blanks",
    3: "📝 Title & Points"
}