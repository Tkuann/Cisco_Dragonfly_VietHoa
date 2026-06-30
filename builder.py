import json
import shutil
import zipfile

from config import TRANSLATED_FOLDER, RESOURCEPACK_FOLDER, ROOT

PACK_NAME = "Cisco Dragonfly Viet Hoa"
PACK_FORMAT = 15
ZIP_NAME = "Cisco_Dragonfly_Viet_Hoa.zip"


def detect_modid(filename):
    return filename.stem


def zip_folder(folder, zip_path):
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in folder.rglob("*"):
            if file.is_file():
                zipf.write(file, file.relative_to(folder))


def main():
    if RESOURCEPACK_FOLDER.exists():
        shutil.rmtree(RESOURCEPACK_FOLDER)

    assets_folder = RESOURCEPACK_FOLDER / "assets"
    assets_folder.mkdir(parents=True, exist_ok=True)

    pack_mcmeta = {
        "pack": {
            "pack_format": PACK_FORMAT,
            "description": PACK_NAME
        }
    }

    with open(RESOURCEPACK_FOLDER / "pack.mcmeta", "w", encoding="utf-8") as f:
        json.dump(pack_mcmeta, f, ensure_ascii=False, indent=2)

    files = sorted(TRANSLATED_FOLDER.glob("*.json"))

    if not files:
        print("Không tìm thấy file đã dịch trong 03_Translated")
        return

    count = 0

    for file in files:
        modid = detect_modid(file)
        lang_folder = assets_folder / modid / "lang"
        lang_folder.mkdir(parents=True, exist_ok=True)

        output_file = lang_folder / "vi_vn.json"
        shutil.copyfile(file, output_file)

        print(f"Đã thêm: {modid}/lang/vi_vn.json")
        count += 1

    zip_path = ROOT / ZIP_NAME
    zip_folder(RESOURCEPACK_FOLDER, zip_path)

    print()
    print("Hoàn thành Resource Pack")
    print("Số file:", count)
    print("Thư mục:", RESOURCEPACK_FOLDER)
    print("File ZIP:", zip_path)


if __name__ == "__main__":
    main()