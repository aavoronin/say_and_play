import os

class execute_and_cache_helper:
    def __init__(self):
        pass

    @staticmethod
    def try_load_from_cache_text(fname):
        if os.path.exists(fname) and os.path.getsize(fname) > 0:
            with open(fname, "r", encoding="utf-8") as f:
                s = f.read()
                f.close()
                return s
        return None

    @staticmethod
    def save_to_cache_text(fname, text):
        with open(fname, "w", encoding="utf-8") as f:
            f.write(text)
            f.close()

