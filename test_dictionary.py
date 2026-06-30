from dictionary import DictionaryManager

d = DictionaryManager()

tests = [
    ("UI", "{6} Damage"),
    ("ITEM", "Shadowwalker Boots"),
    ("ITEM", "Ancient Spellbook"),
    ("SPELL", "Fireball"),
    ("EFFECT", "Chilled")
]

for context, text in tests:
    print(context, text, "=>", d.translate_by_context(context, text))