import win32gui
import keyboard
# Load all images in the directory
import os
from PIL import Image
import cv2
import numpy as np
import pyautogui
import time


#pip install pywin32
DELAY = 0.5
time.sleep(10.0)

class TextToSpeechHelper:
    def __init__(self, lang):
        self.lang = lang
        self.url = "https://cloud.google.com/text-to-speech?hl=ru#demo"

    def activate_window(self):
        substring = 'Text-to-Speech'

        def enum_handler(hwnd, result):
            if win32gui.IsWindowVisible(hwnd):
                result.append((hwnd, win32gui.GetWindowText(hwnd)))
            return True

        result = []
        win32gui.EnumWindows(enum_handler, result)
        for hwnd, title in result:
            if substring in title:
                win32gui.SetForegroundWindow(hwnd)



    def select_language(self, lang):
        lang_selector_info = {
            "en": {"l": "e", "d": 3, "v": 1},
            #en": {"l": "e", "d": 3, "v": 8},
            "ja": {"l": "日", "d": 0, "v": 2},
            "ko": {"l": "한", "d": 0, "v": 2},
            "ru": {"l": "р", "d": 0, "v": 1},
            "es": {"l": "e", "d": 4, "v": 1},
            "de": {"l": "d", "d": 1, "v": 1},
            "fr": {"l": "f", "d": 2, "v": 1},
            "it": {"l": "i", "d": 0, "v": 3},
            "pt": {"l": "p", "d": 2, "v": 1},
            "vi": {"l": "t", "d": 0, "v": 3},
            "th": {"l": "ไ", "d": 0, "v": 0},
            "pl": {"l": "p", "d": 0, "v": 2},
            "cs": {"l": "Č", "d": 0, "v": 0},
            "ar": {"l": "a", "d": 1, "v": 2},
                # used_langs = ["en", "ja", "ko", "ru", "es", "de", "fr", "it", "pt", "vi", "th", "pl", "cs", "ar"]
        }
        self.press_tab(2)
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        sel = lang_selector_info[lang]
        keyboard.write(sel["l"])
        for _ in range(sel["d"]):
            pyautogui.press('down')
            time.sleep(0.2)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(0.5)
        self.press_tab(2)
        pyautogui.press('enter')
        for _ in range(sel["v"]):
            pyautogui.press('down')
            time.sleep(0.2)
        time.sleep(1)
        pyautogui.press('enter')


    def press_tab(self, n):
        for _ in range(n):
            pyautogui.press('tab')
            time.sleep(DELAY)
    def press_shift_tab(self, n):
        for _ in range(n):
            pyautogui.hotkey('shift', 'tab')
            time.sleep(DELAY)

    def return_to_text(self):
        self.press_shift_tab(2)
        self.press_shift_tab(2)

    def pronounce(self, text_to_type):
        # Press Ctrl+A
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(DELAY)

        # Press Del
        pyautogui.press('delete')
        time.sleep(DELAY)

        # Type text from the variable chunk
        # pyautogui.write(text_to_type)
        # Type the text
        keyboard.write(text_to_type)
        time.sleep(DELAY)

        # Press Tab 10 times
        for _ in range(9):
            pyautogui.press('tab')
            time.sleep(DELAY)

        pyautogui.press('enter')
        time.sleep(DELAY)

        self.play_loop()

        # Press Shift+Tab 10 times
        for _ in range(9):
            pyautogui.hotkey('shift', 'tab')
            time.sleep(DELAY)

    def play_loop(self):
        # Define the directory containing the images
        dir_path = "images/"
        # Load all images in the directory
        images = [(Image.open(os.path.join(dir_path, f)), f) for f in os.listdir(dir_path) if
                  f.endswith('.png') or f.endswith('.jpg')]
        prev = ''
        founds = 0
        while True:
            # Take screenshot
            screenshot = pyautogui.screenshot()

            # Convert screenshot to numpy array and grayscale
            screenshot_np = np.array(screenshot)
            screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

            d = dict()
            # Iterate over all images
            for img, filename in images:
                # Convert image to grayscale
                img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

                # Use template matching to find the image in the screenshot
                res = cv2.matchTemplate(screenshot_gray, img_gray, cv2.TM_CCOEFF_NORMED)
                d[filename] = res.max()

            print(d)
            detected = [(key, d[key]) for key in d.keys() if (d[key] > 0.93 and key == 'Replay.png') or d[key] > 0.986]
            detected = sorted(detected, reverse=True)
            if len(detected) > 0:
                k = detected[0][0]
                if k == prev:
                    founds += 1
                else:
                    prev = k
                    founds = 0

            print(prev, founds)
            if prev.startswith('Replay') and founds > 6:
                break

            # Wait for 0.5 seconds before the next iteration
            time.sleep(0.5)
            pass

    @classmethod
    def get_max_expected_recording_time(cls, lang, translation):
        l = len(translation)
        if lang in ["ja", "ko", "he", "th"]:
            l *= 2
        if l > 800:
            return 120
        if l > 400:
            return 90
        if l > 250:
            return 60
        return 60




