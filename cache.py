import json

from config import CACHE_FILE


class TranslationCache:

    def __init__(self):
        self.cache = self.load()

    def load(self):

        if not CACHE_FILE.exists():
            return {}

        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self):

        with open(CACHE_FILE, "w", encoding="utf-8") as f:

            json.dump(
                self.cache,
                f,
                ensure_ascii=False,
                indent=2
            )

    def has(self, text):

        return text in self.cache

    def get(self, text):

        return self.cache[text]

    def add(self, source, translated):

        self.cache[source] = translated

    def size(self):

        return len(self.cache)