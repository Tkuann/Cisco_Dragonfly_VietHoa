from glossary import Glossary
from translator import translate_text

glossary = Glossary()

texts = [
    "Ancient Spellbook",
    "Greater Fire Spell",
    "Shadowwalker Boots",
    "Mana Regen"
]

for text in texts:
    if glossary.has(text):
        result = glossary.get(text)
    else:
        terms = glossary.find_terms(text)
        result = translate_text(text, terms)

    print(text, "=>", result)