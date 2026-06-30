from translator import translate_batch

texts = [
    "Fireball",
    "Health",
    "Mana",
    "Spellbook"
]

result = translate_batch(texts)

print(result)