import json

from config import DICTIONARY_FOLDER


class DictionaryManager:

    def __init__(self):
        self.ui = self.load_dictionary("ui.json")
        self.item = self.load_dictionary("item.json")
        self.spell = self.load_dictionary("spell.json")
        self.effect = self.load_dictionary("effect.json")

    def load_dictionary(self, filename):
        path = DICTIONARY_FOLDER / filename

        if not path.exists():
            return {}

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def replace_terms(self, text, dictionary):
        result = text

        terms = sorted(
            dictionary.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )

        changed = False

        for source, target in terms:
            if source in result:
                result = result.replace(source, target)
                changed = True

        if changed:
            return result

        return None

    def translate_ui(self, text):
        return self.replace_terms(text, self.ui)

    def translate_item(self, text):
        return self.replace_terms(text, self.item)

    def translate_spell(self, text):
        return self.replace_terms(text, self.spell)

    def translate_effect(self, text):
        return self.replace_terms(text, self.effect)

    def translate_by_context(self, context, text):
        if context == "UI":
            return self.translate_ui(text)

        if context == "ITEM":
            return self.translate_item(text)

        if context == "SPELL":
            return self.translate_spell(text)

        if context == "EFFECT":
            return self.translate_effect(text)

        return None