import hashlib
import os
import shutil
from TranslationsHelper import ensure_folder_exists
from pydub import AudioSegment

class SoundHelper:
    @classmethod
    def get_filename_for(cls, lang, translation):
        cache_name = f'{lang} w={translation}'
        filename = hashlib.md5(cache_name.encode()).hexdigest() + '.mp3'
        cache_folder = f"c:/Cache/Sounds/{lang}"
        ensure_folder_exists(cache_folder)
        filepath = os.path.join(cache_folder, filename).replace("/", "\\")
        return filepath


    @classmethod
    def remove_silence(cls, mp3_file_name, min_len_secs=0):
        margin_secs = 0.3
        margin_pieces = int(margin_secs / 0.1)
        silense_DBs = 4

        out_mp3_file_name = mp3_file_name.replace('.mp3', '_out.mp3')

        # Load MP3 file
        sound = AudioSegment.from_mp3(mp3_file_name)

        # Split the audio into 0.1-second pieces
        chunks = [sound[i:i + 100] for i in range(0, len(sound), 100)]

        # Calculate decibels for each chunk
        decibels = [abs(chunk.dBFS) if chunk.dBFS > -200 and chunk.dBFS < +200 else 0 for chunk in chunks]

        # Ignore 3 consecutive pieces with highest decibels < 10 from the beginning
        start_index = 0
        while start_index < len(decibels) - margin_pieces and max(decibels[start_index:start_index + margin_pieces]) < 10:
            start_index += 1

        # Ignore 3 consecutive pieces with highest decibels < 10 from the end
        end_index = len(decibels)
        while end_index > margin_pieces and max(decibels[end_index - margin_pieces:end_index]) < silense_DBs:
            end_index -= 1

        while end_index - start_index < min_len_secs * 10:
            end_index += 1

        # Combine the remaining non-silent chunks and export as output file
        non_silent_sound = sum(chunks[start_index:end_index], AudioSegment.empty())
        non_silent_sound.export(out_mp3_file_name, format="mp3")

        # Copy file_name2 over to file_name, overwriting it
        shutil.copy2(out_mp3_file_name, mp3_file_name)

        # Delete file_name2
        os.remove(out_mp3_file_name)
