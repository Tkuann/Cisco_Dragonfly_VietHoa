import json

from config import DICTIONARY_FOLDER


class DictionaryManager:

    def __init__(self):
        self.master = self.load_dictionary("master_rpg.json")
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

    def exact_lookup(self, text, dictionary):
        return dictionary.get(text)

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

    def translate_by_context(self, context, text):
        if context == "UI":
            exact = self.exact_lookup(text, self.ui)
            if exact:
                return exact

        if context == "ITEM":
            exact = self.exact_lookup(text, self.item)
            if exact:
                return exact

        if context == "SPELL":
            exact = self.exact_lookup(text, self.spell)
            if exact:
                return exact

        if context == "EFFECT":
            exact = self.exact_lookup(text, self.effect)
            if exact:
                return exact

        exact_master = self.exact_lookup(text, self.master)
        if exact_master:
            return exact_master

        context_dict = None

        if context == "UI":
            context_dict = self.ui
        elif context == "ITEM":
            context_dict = self.item
        elif context == "SPELL":
            context_dict = self.spell
        elif context == "EFFECT":
            context_dict = self.effect

        if context_dict:
            context_result = self.replace_terms(text, context_dict)
            if context_result:
                return context_result

        master_result = self.replace_terms(text, self.master)
        if master_result:
            return master_result

        return None