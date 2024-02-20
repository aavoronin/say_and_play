import hashlib
import os
import urllib
from urllib.parse import quote

from deep_translator import GoogleTranslator

from WebHelper import WebHelper
from execute_and_cache_helper import execute_and_cache_helper
from string_helper import edit_distance


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


    @staticmethod
    def encode_url(url):
        # Split the URL into components
        scheme, netloc, path, params, query, fragment = urllib.parse.urlparse(url)

        # Encode the path component
        encoded_path = quote(path.encode('utf-8'), safe=':/')

        # Reconstruct the URL with the encoded path
        encoded_url = urllib.parse.urlunparse((scheme, netloc, encoded_path, params, query, fragment))

        return encoded_url

    @staticmethod
    def find_text_between_b_tags(text, max_length):
        # Define the pattern to match text between <b> and </b> tags, excluding nested tags
        pattern = r'<p><b>(?:[^<>]|<(?!/b>))*?<\/b>'
        # Find matches and filter by length
        matches = [match[len('<p><b>'):-len('</b>')] for match in re.findall(pattern, str(text))]
        return matches

    @classmethod
    def find_prononciation(cls, text, lang):

        langs_to_exclude = [l for l in used_langs if l not in ["ru"]] #["ja", "en", "ko"]
        if lang in langs_to_exclude:
            return text

        cache_path = f"c:/Cache/prononciations/{lang}"
        ensure_folder_exists(cache_path)
        cache_name = f"{lang} {text}"
        md5 = hashlib.md5(cache_name.encode('utf-8')).hexdigest()
        fname = f"{cache_path}\\{str(md5)}.txt"
        result = execute_and_cache_helper.try_load_from_cache_text(fname)
        if result is not None:
            return result

        result = cls.download_wikipedia_url_for_name_lang(lang, text)
        if result is not None:
            matches = TranslationsHelper.find_text_between_b_tags(result, len(text))
            if len(matches) > 0:
                edit_d = edit_distance(text, matches[0])
                if edit_d > 0 and edit_d <= 4 + len(text) // 5:
                    text = matches[0]
        execute_and_cache_helper.save_to_cache_text(fname, text)
        return text

    @classmethod
    def download_wikipedia_url_for_name_lang(cls, lang, text):
        try:
            result = WebHelper.download_url(f"https://{lang}.wikipedia.org/wiki/{TranslationsHelper.encode_url(text)}")
            return result
        except Exception as e:
            print(f"{text} - Download attempt failed: {e}")
        return None


global_translators = dict()
for lang in used_langs:
    global_translators[lang] = TranslationsHelper(lang)