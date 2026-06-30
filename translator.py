import json
import re
import time
import urllib.request

from config import MODEL, PROMPT_FILE

OLLAMA_URL = "http://localhost:11434/api/generate"


def load_prompt():
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text(encoding="utf-8")
    return ""


def has_cjk(text):
    return bool(re.search(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", str(text)))


def clean_text(text):
    text = text.strip()
    text = text.replace("```", "")
    text = text.replace('"', "")
    return text.strip()


def call_ollama_single(text, terms=None, context_note=""):
    terms = terms or {}

    glossary_text = ""

    if terms:
        glossary_text = "\nTHUẬT NGỮ BẮT BUỘC:\n"
        for source, target in terms.items():
            glossary_text += f"- {source} = {target}\n"

    prompt = f"""
{load_prompt()}

NGỮ CẢNH:
{context_note}

{glossary_text}

Dịch chuỗi sau sang tiếng Việt.

YÊU CẦU:
- Chỉ trả về đúng bản dịch.
- Không giải thích.
- Không markdown.
- Không dùng tiếng Trung, Nhật, Hàn.
- Giữ nguyên %s %d {{0}} {{1}} \\n §a §b §c §6.
- Nếu là chữ giao diện, dịch ngắn gọn.
- Nếu là tên vật phẩm/phép, dịch theo phong cách RPG Fantasy.

INPUT:
{text}

OUTPUT:
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req, timeout=300) as response:
        data = json.loads(response.read().decode("utf-8"))

    result = clean_text(data["response"])

    if has_cjk(result):
        raise ValueError("Phát hiện tiếng Trung/Nhật/Hàn.")

    if not result:
        raise ValueError("Kết quả rỗng.")

    return result


def translate_text(text, terms=None, context_note=""):
    for attempt in range(3):
        try:
            return call_ollama_single(text, terms, context_note)
        except Exception as e:
            print(f"  Lỗi dịch '{text}' lần {attempt + 1}/3:", e)
            time.sleep(1)

    return text


# ==========================================
# Batch API
# ==========================================

def translate_batch(texts, terms_list=None, context_list=None):
    """
    Batch translator.
    Hiện tại để tương thích Engine cũ nên vẫn dịch tuần tự.
    Sau này chỉ cần sửa hàm này là toàn bộ Engine sẽ nhanh lên.
    """

    if not texts:
        return []

    if terms_list is None:
        terms_list = [None] * len(texts)

    if context_list is None:
        context_list = [""] * len(texts)

    results = []

    for text, terms, context in zip(texts, terms_list, context_list):
        result = translate_text(
            text,
            terms,
            context
        )
        results.append(result)

    return results