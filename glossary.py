import json

from config import GLOSSARY_FILE


class Glossary:

    def __init__(self):
        self.terms = self.load()

    def load(self):
        if not GLOSSARY_FILE.exists():
            return {}

        with open(GLOSSARY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def has(self, text):
        return text in self.terms

    def get(self, text):
        return self.terms[text]

    def size(self):
        return len(self.terms)

    def find_terms(self, text):
        found = {}

        lower_text = text.lower()

        for source, target in self.terms.items():
            if source.lower() in lower_text:
                found[source] = target

        return found