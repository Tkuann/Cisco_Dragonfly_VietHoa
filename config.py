from pathlib import Path

# ==========================
# Root
# ==========================

ROOT = Path(__file__).parent.resolve()

# ==========================
# Folders
# ==========================

MOD_FOLDER = ROOT / "01_Mod_Files"
EXTRACT_FOLDER = ROOT / "02_Extract"
TRANSLATED_FOLDER = ROOT / "03_Translated"
RESOURCEPACK_FOLDER = ROOT / "04_ResourcePack"
CACHE_FOLDER = ROOT / "05_Cache"
LOG_FOLDER = ROOT / "06_Logs"
BACKUP_FOLDER = ROOT / "07_Backup"
DICTIONARY_FOLDER = ROOT / "07_Dictionaries"

# ==========================
# Files
# ==========================

CACHE_FILE = CACHE_FOLDER / "translation_cache.json"
PROMPT_FILE = ROOT / "prompt.txt"
GLOSSARY_FILE = ROOT / "glossary.json"

# ==========================
# Translation
# ==========================

MODEL = "qwen2.5:7b"
BATCH_SIZE = 5
MAX_RETRY = 3
REQUEST_DELAY = 1.0

# ==========================
# Auto Create
# ==========================

for folder in (
    MOD_FOLDER,
    EXTRACT_FOLDER,
    TRANSLATED_FOLDER,
    RESOURCEPACK_FOLDER,
    CACHE_FOLDER,
    LOG_FOLDER,
    BACKUP_FOLDER,
    DICTIONARY_FOLDER,
):
    folder.mkdir(exist_ok=True)

if not CACHE_FILE.exists():
    CACHE_FILE.write_text("{}", encoding="utf-8")