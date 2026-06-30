import json
from pathlib import Path

from config import TRANSLATED_FOLDER, DICTIONARY_FOLDER


def load_json(path):
    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    overrides_path = DICTIONARY_FOLDER / "key_overrides.json"
    overrides = load_json(overrides_path)

    files = sorted(TRANSLATED_FOLDER.glob("*.json"))

    if not files:
        print("Chưa có file dịch trong 03_Translated")
        return

    print("\nDanh sách file đã dịch:\n")

    for i, file in enumerate(files, start=1):
        print(f"{i}. {file.name}")

    print()

    choice = input("Chọn file để áp dụng override: ").strip()

    if not choice.isdigit():
        print("Lựa chọn không hợp lệ.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(files):
        print("Số file không hợp lệ.")
        return

    target_path = files[index]
    data = load_json(target_path)

    changed = 0

    for key, value in overrides.items():
        if key in data and data[key] != value:
            data[key] = value
            changed += 1

    save_json(target_path, data)

    print("=" * 60)
    print("File:", target_path.name)
    print("Đã áp dụng override:", changed)
    print("=" * 60)


if __name__ == "__main__":
    main()