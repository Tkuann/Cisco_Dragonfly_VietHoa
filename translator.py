import json
import re
import time
import urllib.request

from config import MODEL, PROMPT_FILE

OLLAMA_URL = "http://localhost:11434/api/generate"


# Những cụm cực phổ biến xử lý thẳng, không gửi AI.
# Mục tiêu: tránh lỗi model dịch lệch như Fireball -> Bola Lửa.
COMMON_EXACT = {
    "Fireball": "Hỏa cầu",
    "Health": "Sinh lực",
    "Mana": "Mana",
    "Spellbook": "Ma đạo thư",
    "Spell Book": "Ma đạo thư",
    "Spell": "Phép thuật",
    "Cooldown": "Thời gian hồi chiêu",
    "Cast": "Thi triển",
    "Cast Time": "Thời gian niệm",
    "Spell Power": "Sức mạnh phép thuật",
    "Magic Missile": "Đạn Phép Ma Thuật",
    "Teleport": "Dịch Chuyển",
    "Raise Dead": "Triệu Hồi Vong Linh",
    "Firebolt": "Hỏa tiễn",
    "Fire Breath": "Hơi Thở Lửa",
    "Wall of Fire": "Tường Lửa",
    "Blaze Storm": "Bão Lửa",
    "Counterspell": "Phản Phép",
    "Pocket Dimension": "Không Gian Bỏ Túi",
}


def load_prompt():
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text(encoding="utf-8")
    return ""


def has_cjk(text):
    return bool(re.search(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", str(text)))


def strip_prompt_leak(text):
    """
    Loại bỏ các phần model hay trả thêm như OUTPUT, Note, Explanation...
    Chỉ giữ lại phần giống bản dịch nhất.
    """
    text = str(text).strip()
    text = text.replace("```", "")
    text = text.replace('"', "")

    # Nếu model lặp lại OUTPUT:, lấy phần sau OUTPUT cuối cùng.
    output_markers = ["OUTPUT:", "Output:", "Đầu ra:"]
    for marker in output_markers:
        if marker in text:
            text = text.split(marker)[-1].strip()

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    bad_starts = (
        "INPUT:",
        "Input:",
        "Note:",
        "NOTE:",
        "Explanation:",
        "Reason:",
        "Giải thích:",
        "Dịch lại chính xác:",
        "Đầu ra chỉ bao gồm bản dịch",
        "THUẬT NGỮ",
        "YÊU CẦU",
        "Merge key",
        "The input",
        "If more context",
    )

    cleaned = []

    for line in lines:
        if line.startswith(bad_starts):
            continue

        if line.startswith("- "):
            continue

        if line.lower().startswith("note"):
            continue

        cleaned.append(line)

    if not cleaned:
        return ""

    # Ưu tiên dòng đầu tiên còn lại sau OUTPUT.
    # Không lấy dòng cuối vì nhiều model đặt ghi chú sau bản dịch.
    result = cleaned[0].strip()

    # Nếu model trả dạng "Bản dịch: xxx"
    prefixes = [
        "Bản dịch:",
        "Dịch:",
        "Translation:",
        "Vietnamese:",
    ]

    for prefix in prefixes:
        if result.startswith(prefix):
            result = result[len(prefix):].strip()

    result = result.replace("```", "")
    result = result.replace('"', "")
    result = re.sub(r"\s+", " ", result).strip()

    return result


def clean_text(text):
    result = strip_prompt_leak(text)

    # Cắt bỏ phần ghi chú trong ngoặc nếu model vẫn lỡ thêm.
    result = re.sub(r"\s*\(Note:.*?\)\s*$", "", result, flags=re.IGNORECASE)
    result = re.sub(r"\s*\(.*?specific.*?\)\s*$", "", result, flags=re.IGNORECASE)

    return result.strip()


def is_bad_output(result):
    if not result:
        return True

    bad_fragments = [
        "OUTPUT:",
        "INPUT:",
        "Note:",
        "Explanation:",
        "Reason:",
        "Merge key",
        "THUẬT NGỮ",
        "YÊU CẦU",
        "Dịch chuỗi sau",
        "Đầu ra chỉ bao gồm",
    ]

    for fragment in bad_fragments:
        if fragment in result:
            return True

    # Không chấp nhận kết quả quá dài bất thường cho input ngắn.
    if len(result) > 500:
        return True

    return False


def call_ollama_single(text, terms=None, context_note=""):
    text = str(text).strip()

    if text in COMMON_EXACT:
        return COMMON_EXACT[text]

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

NHIỆM VỤ:
Dịch chính xác INPUT sang tiếng Việt.

QUY TẮC BẮT BUỘC:
- Chỉ trả về đúng một bản dịch tiếng Việt.
- Không giải thích.
- Không ghi chú.
- Không markdown.
- Không lặp lại INPUT.
- Không viết OUTPUT:
- Không dùng tiếng Trung, Nhật, Hàn.
- Không dùng tiếng Indonesia.
- Giữ nguyên %s %d %1$s %2$s {{0}} {{1}} \\n §a §b §c §6 %%.
- Nếu là tên vật phẩm/phép, dịch theo phong cách RPG Fantasy.

INPUT:
{text}

BẢN DỊCH:
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "top_p": 0.7,
            "repeat_penalty": 1.2
        }
    }

    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req, timeout=300) as response:
        data = json.loads(response.read().decode("utf-8"))

    result = clean_text(data["response"])

    if is_bad_output(result):
        raise ValueError("Kết quả chứa prompt leak hoặc rỗng.")

    if has_cjk(result):
        raise ValueError("Phát hiện tiếng Trung/Nhật/Hàn.")

    return result


def translate_text(text, terms=None, context_note=""):
    text = str(text).strip()

    if text in COMMON_EXACT:
        return COMMON_EXACT[text]

    for attempt in range(3):
        try:
            return call_ollama_single(text, terms, context_note)
        except Exception as e:
            print(f"  Lỗi dịch '{text}' lần {attempt + 1}/3:", e)
            time.sleep(1)

    return text


def translate_batch(texts, terms_list=None, context_list=None):
    if not texts:
        return []

    if terms_list is None:
        terms_list = [None] * len(texts)

    if context_list is None:
        context_list = [""] * len(texts)

    results = []

    for text, terms, context in zip(texts, terms_list, context_list):
        result = translate_text(text, terms, context)
        results.append(result)

    return results
