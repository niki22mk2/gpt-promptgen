import pathlib
import json
from constants.constants import OUTPUT_DIR, FIXED_TAGS_FILE

def load_fixed_tags():
    print("Loading fixed tags...")
    if pathlib.Path(FIXED_TAGS_FILE).exists():
        with open(FIXED_TAGS_FILE, 'r') as f:
            tags = json.load(f)
            print(f"[Prompt-Gen] Loaded fixed tags: {tags}")
            return tags
    print("[Prompt-Gen] No fixed tags found")
    return {'prefix': '', 'suffix': ''}

def save_fixed_tags(prefix, suffix):
    output_dir = pathlib.Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(FIXED_TAGS_FILE, 'w') as f:
        json.dump({'prefix': prefix, 'suffix': suffix}, f)
        print(f"[Prompt-Gen] Saved fixed tags: prefix: {prefix}, suffix: {suffix}")