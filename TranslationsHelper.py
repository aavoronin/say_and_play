import hashlib
import os

from deep_translator import GoogleTranslator


def ensure_folder_exists(folder_path):
   # Check if the folder exists
   if not os.path.exists(folder_path):
       # If the folder does not exist, create it
       os.makedirs(folder_path)


used_langs = ["ru", "en", "ja", "ko", "ar", "es", "de", "fr", "it", "pt", "vi", "th", "pl", "cs"]

class TranslationsHelper:
    def __init__(self, lang):
        self.lang = lang
        self.translators = [
                #DeeplTranslator,
                            GoogleTranslator
                #, MyTranslator1
        ]
        self.force_retranslate = []
        self.translated = dict()

    def translate(self, text):
        cache_name = f'{self.lang} w={text}'
        if cache_name in self.translated:
            return self.translated[cache_name]
        filename = hashlib.md5(cache_name.encode()).hexdigest() + '.txt'
        cache_folder = f"c:/Cache/Translations/{self.lang}"
        ensure_folder_exists(cache_folder)
        filepath = os.path.join(cache_folder, filename).replace("/", "\\")
        if os.path.exists(filepath) and text not in self.force_retranslate:
            with open(filepath, "r", encoding="utf-8") as f:
                translated = f.read()
                self.translated[cache_name] = translated
                f.close()
                return translated

        for translator in self.translators:
            try:
                translated = translator(source='en', target=self.lang).translate(text)
                break
            except Exception as e:
                translated = text

        self.translated[cache_name] = translated
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(translated)

        return translated


global_translators = dict()
for lang in used_langs:
    global_translators[lang] = TranslationsHelper(lang)