import json

from cache import TranslationCache
from config import EXTRACT_FOLDER, TRANSLATED_FOLDER
from dictionary import DictionaryManager
from glossary import Glossary
from translation_engine import TranslationEngine


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    path.parent.mkdir(exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def translate_file(input_file, engine):
    print()
    print("=" * 50)
    print(f"Đang dịch: {input_file.name}")
    print("=" * 50)

    data = load_json(input_file)
    result = engine.translate_data(data)

    output_file = TRANSLATED_FOLDER / input_file.name
    save_json(output_file, result)

    print("Đã lưu:", output_file)


def translate_one_file(files, engine):
    print("\nDanh sách file:\n")

    for i, file in enumerate(files, start=1):
        print(f"{i}. {file.name}")

    print()
    choice = input("Chọn file cần dịch: ").strip()

    if not choice.isdigit():
        print("Lựa chọn không hợp lệ.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(files):
        print("Số file không hợp lệ.")
        return

    translate_file(files[index], engine)


def translate_all_files(files, engine):
    print()
    print(f"Bắt đầu dịch toàn bộ {len(files)} file...")

    for index, file in enumerate(files, start=1):
        output_file = TRANSLATED_FOLDER / file.name

        if output_file.exists():
            print(f"\n[{index}/{len(files)}] Bỏ qua {file.name} vì đã dịch.")
            continue

        print(f"\n[{index}/{len(files)}]")
        translate_file(file, engine)

    print()
    print("Đã dịch xong toàn bộ thư mục.")


def main():
    print("=" * 50)
    print("Minecraft Translator Engine v4.0")
    print("=" * 50)

    files = sorted(EXTRACT_FOLDER.glob("*.json"))

    if not files:
        print("Không tìm thấy file JSON trong 02_Extract")
        return

    cache = TranslationCache()
    glossary = Glossary()
    dictionary = DictionaryManager()
    engine = TranslationEngine(cache, glossary, dictionary)

    print()
    print("1. Dịch 1 file")
    print("2. Dịch toàn bộ thư mục")
    print()

    choice = input("Chọn chế độ: ").strip()

    if choice == "1":
        translate_one_file(files, engine)
    elif choice == "2":
        translate_all_files(files, engine)
    else:
        print("Lựa chọn không hợp lệ.")

    print()
    print("Hoàn thành!")


if __name__ == "__main__":
    main()