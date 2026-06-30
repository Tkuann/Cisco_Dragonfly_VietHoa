import json
from config import TRANSLATED_FOLDER


PATCH_FILE = "patch.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    patch_path = TRANSLATED_FOLDER.parent / PATCH_FILE

    if not patch_path.exists():
        print("Không tìm thấy patch.json")
        return

    patch = load_json(patch_path)

    files = sorted(TRANSLATED_FOLDER.glob("*.json"))

    print("\nDanh sách file đã dịch:\n")

    for i, file in enumerate(files, start=1):
        print(f"{i}. {file.name}")

    choice = input("\nChọn file cần patch: ").strip()

    if not choice.isdigit():
        print("Lựa chọn không hợp lệ.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(files):
        print("Số file không hợp lệ.")
        return

    target = files[index]
    data = load_json(target)

    changed = 0
    missing = []

    for key, value in patch.items():
        if key in data:
            data[key] = value
            changed += 1
        else:
            missing.append(key)

    save_json(target, data)

    print("=" * 60)
    print("File:", target.name)
    print("Đã thay:", changed)
    print("Không tìm thấy key:", len(missing))

    if missing:
        print("\n--- KEY KHÔNG TÌM THẤY ---")
        for key in missing[:30]:
            print(key)

    print("=" * 60)


if __name__ == "__main__":
    main()