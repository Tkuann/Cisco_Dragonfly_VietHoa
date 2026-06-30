from cache import TranslationCache

cache = TranslationCache()

print("Ban đầu:", cache.size())

cache.add("Fireball", "Hỏa cầu")

cache.add("Health", "Sinh lực")

cache.save()

cache = TranslationCache()

print("Sau khi load:", cache.size())

print(cache.get("Fireball"))

print(cache.get("Health"))