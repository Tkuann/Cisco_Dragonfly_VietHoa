from collections import defaultdict

from context import detect_context, context_instruction
from key_overrides import KeyOverrides
from translator import translate_text


class TranslationEngine:

    def __init__(self, cache, glossary, dictionary):
        self.cache = cache
        self.glossary = glossary
        self.dictionary = dictionary
        self.key_overrides = KeyOverrides()

    def translate_data(self, data):
        translated = {}
        waiting = defaultdict(list)

        for key, value in data.items():

            if self.key_overrides.has(key):
                result = self.key_overrides.get(key)
                translated[key] = result
                self.cache.add(value, result)
                continue

            if self.cache.has(value):
                translated[key] = self.cache.get(value)
                continue

            if self.glossary.has(value):
                result = self.glossary.get(value)
                translated[key] = result
                self.cache.add(value, result)
                continue

            context = detect_context(key)
            dict_result = self.dictionary.translate_by_context(context, value)

            if dict_result:
                translated[key] = dict_result
                self.cache.add(value, dict_result)
                continue

            waiting[value].append(key)

        unique_texts = list(waiting.keys())

        print("Tổng dòng        :", len(data))
        print("Đã xử lý sẵn     :", len(translated))
        print("Cần AI dịch      :", len(unique_texts))

        total = len(unique_texts)

        for index, source in enumerate(unique_texts, start=1):
            print(f"[{index}/{total}] {source}")

            sample_key = waiting[source][0]
            context = detect_context(sample_key)
            context_note = context_instruction(context)
            terms = self.glossary.find_terms(source)

            target = translate_text(source, terms, context_note)

            self.cache.add(source, target)

            for key in waiting[source]:
                translated[key] = target

            self.cache.save()

        result = {}

        for key, value in data.items():
            if key in translated:
                result[key] = translated[key]
            elif self.cache.has(value):
                result[key] = self.cache.get(value)
            else:
                result[key] = value

        self.cache.save()

        return result