import json
import re
from pathlib import Path

from config import TRANSLATED_FOLDER

CJK_PATTERN = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]")
ENGLISH_PATTERN = re.compile(r"[A-Za-z]{3,}")


def has_cjk(text):
    return bool(CJK_PATTERN.search(str(text)))


def has_english(text):
    text = str(text)

    allowed = {
        "Mana",
        "Ender",
        "Netherite",
        "Diamond",
        "Iron",
        "Gold",
        "Copper",
        "Emerald",
        "Ruby",
        "Sapphire",
        "Pyrium",
        "Mithril",
        "Druid",
        "Minecraft",
        "HP",
        "AOE",
        "Boss"
    }

    suspicious = {
        "Dropped",
        "Drop",
        "Use",
        "Using",
        "Spell",
        "Spellbook",
        "Book",
        "Guide",
        "Upgrade",
        "Improvement",
        "Capacity",
        "Slot",
        "Armor",
        "Robe",
        "Boots",
        "Helmet",
        "Chestplate",
        "Leggings",
        "Hat",
        "Hood",
        "Staff",
        "Sword",
        "Bow",
        "Ring",
        "Amulet",
        "Rune",
        "Potion",
        "Splash",
        "Lingering",
        "Arrow",
        "Spawn",
        "Egg",
        "Magic",
        "Resistance",
        "Cooldown",
        "Recovery",
        "Fire",
        "Ice",
        "Lightning",
        "Blood",
        "Holy",
        "Nature",
        "Arcane",
        "Void",
        "Eldritch",
        "Wizard",
        "Mage",
        "Battlemage",
        "Pyromancer",
        "Cryomancer",
        "Electromancer",
        "Necromancer",
        "Shadowwalker",
        "Archevoker",
        "Blank",
        "Protective",
        "Improves",
        "of"
    }

    words = re.findall(r"[A-Za-z]+", text)

    for word in words:
        if word in allowed:
            continue

        if word in suspicious:
            return True

    return False


def check_file(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cjk_errors = []
    english_warnings = []

    for key, value in data.items():
        if has_cjk(value):
            cjk_errors.append((key, value))

        if has_english(value):
            english_warnings.append((key, value))

    print("=" * 60)
    print("QA:", path.name)
    print("=" * 60)

    print("Dòng có Trung/Nhật/Hàn:", len(cjk_errors))
    print("Dòng còn tiếng Anh    :", len(english_warnings))

    if cjk_errors:
        print("\n--- LỖI CJK ---")
        for key, value in cjk_errors[:50]:
            print(f"{key}: {value}")

    if english_warnings:
        print("\n--- CÒN TIẾNG ANH ---")
        for key, value in english_warnings[:80]:
            print(f"{key}: {value}")


def main():
    files = sorted(TRANSLATED_FOLDER.glob("*.json"))

    if not files:
        print("Chưa có file dịch trong 03_Translated")
        return

    print("\nDanh sách file đã dịch:\n")

    for i, file in enumerate(files, start=1):
        print(f"{i}. {file.name}")

    print()

    choice = input("Chọn file QA: ").strip()

    if not choice.isdigit():
        print("Lựa chọn không hợp lệ.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(files):
        print("Số file không hợp lệ.")
        return

    check_file(files[index])


if __name__ == "__main__":
    main()