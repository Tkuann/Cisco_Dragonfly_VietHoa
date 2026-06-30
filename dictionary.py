import json
from pathlib import Path

from config import DICTIONARY_FOLDER


class DictionaryManager:

    def __init__(self):
        self.dictionaries = {}

        for file in sorted(Path(DICTIONARY_FOLDER).glob("*.json")):
            with open(file, "r", encoding="utf-8") as f:
                self.dictionaries[file.stem] = json.load(f)

    def exact_lookup(self, text):
        for dictionary in self.dictionaries.values():
            if text in dictionary:
                return dictionary[text]

        return None

    def replace_lookup(self, text):
        result = text
        changed = False

        for dictionary in self.dictionaries.values():
            terms = sorted(
                dictionary.items(),
                key=lambda x: len(x[0]),
                reverse=True
            )

            for source, target in terms:
                if source in result:
                    result = result.replace(source, target)
                    changed = True

        if changed:
            return result

        return None

    def translate_by_context(self, context, text):
        exact = self.exact_lookup(text)

        if exact:
            return exact

        replaced = self.replace_lookup(text)

        if replaced:
            return replaced

        return None