from glossary import Glossary

glossary = Glossary()

tests = [
    "Ancient Spellbook",
    "Fire Spell",
    "Greater Fire Spell",
    "Lightning Bolt",
    "Mana Regen"
]

for text in tests:
    print(text, "=>", glossary.translate_phrase(text))