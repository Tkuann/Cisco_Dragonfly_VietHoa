import json
import re
from config import CACHE_FILE

def has_cjk(text):
    return bool(re.search(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", str(text)))

with open(CACHE_FILE, "r", encoding="utf-8") as f:
    cache = json.load(f)

new_cache = {}
removed = 0

for k, v in cache.items():
    if has_cjk(v):
        removed += 1
    else:
        new_cache[k] = v

with open(CACHE_FILE, "w", encoding="utf-8") as f:
    json.dump(new_cache, f, ensure_ascii=False, indent=2)

print("Đã xóa bản dịch lỗi:", removed)
print("Cache còn lại:", len(new_cache))