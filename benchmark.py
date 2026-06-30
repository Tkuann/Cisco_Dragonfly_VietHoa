import time
from translator import translate_text

tests = [
    "Fireball",
    "Mana",
    "Spellbook",
    "Health",
    "Lightning Bolt",
    "Cooldown",
    "Damage",
    "Arcane Spell",
    "Ice Magic",
    "Blood Magic"
]

start = time.time()

for t in tests:
    print(translate_text(t))

print()
print("Time:", round(time.time() - start, 2), "seconds")