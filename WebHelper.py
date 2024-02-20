import requests
import time

n_downloads = 0
class WebHelper:
    @staticmethod
    def download_url(url):
        global n_downloads
        max_attempts = 5
        result = None
        for attempt in range(max_attempts):
            try:
                n_downloads += 1
                if n_downloads % 50 == 0:
                    time.sleep(120)
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception if the GET request was unsuccessful
                result = response.text  # Return the content of the response if successful
                break
            except Exception as e:
                print(f"Download attempt {attempt + 1} failed: {e}")
                if attempt < max_attempts - 1:  # Do not wait on the last attempt
                    time.sleep(10)  # Wait for  10 seconds before the next attempt

        return result

