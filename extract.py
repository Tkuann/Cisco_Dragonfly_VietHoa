import zipfile
import shutil

from config import MOD_FOLDER, EXTRACT_FOLDER


LANG_FILES = [
    "lang/en_us.json",
    "lang/en_us.lang",
    "lang/en_us.json5"
]


def main():
    EXTRACT_FOLDER.mkdir(exist_ok=True)

    jar_files = sorted(MOD_FOLDER.glob("*.jar"))

    print("=" * 40)
    print(f"Tìm thấy {len(jar_files)} mod")
    print("=" * 40)

    success = 0
    failed = 0
    skipped = 0

    for index, jar_path in enumerate(jar_files, start=1):
        print(f"[{index}/{len(jar_files)}] {jar_path.name}")

        try:
            with zipfile.ZipFile(jar_path) as jar:
                found = False

                for file in jar.namelist():
                    for lang in LANG_FILES:
                        if file.endswith(lang):
                            parts = file.split("/")

                            if len(parts) < 2:
                                continue

                            modid = parts[1]
                            output_file = EXTRACT_FOLDER / f"{modid}.json"

                            if output_file.exists():
                                print(f"    Bỏ qua -> {modid}.json đã tồn tại")
                                skipped += 1
                                found = True
                                break

                            with jar.open(file) as src:
                                with open(output_file, "wb") as dst:
                                    shutil.copyfileobj(src, dst)

                            print(f"    Extracted -> {modid}.json")
                            success += 1
                            found = True
                            break

                    if found:
                        break

                if not found:
                    print("    Không có en_us")

        except Exception as e:
            failed += 1
            print("    Lỗi:", e)

    print()
    print("=" * 40)
    print("Hoàn thành")
    print("=" * 40)
    print("Tổng mod   :", len(jar_files))
    print("Extract mới:", success)
    print("Bỏ qua     :", skipped)
    print("Lỗi        :", failed)


if __name__ == "__main__":
    main()