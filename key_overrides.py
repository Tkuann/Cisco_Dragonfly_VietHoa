import json
from config import DICTIONARY_FOLDER

class KeyOverrides:
    def __init__(self):
        self.data = self.load()

    def load(self):
        path = DICTIONARY_FOLDER / "key_overrides.json"
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def has(self, key):
        return key in self.data

    def get(self, key):
        return self.data[key]