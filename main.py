import os
import random

import numpy as np
import pandas as pd
import time

import librosa as librosa
import sounddevice as sd
from scipy.io.wavfile import write

from pydub import AudioSegment

from pydub import AudioSegment

import countries
from AudioRecorder import AudioRecorder
from SoundHelper import SoundHelper
from TextToSpeechHelper import TextToSpeechHelper
from TranslationsHelper import used_langs, global_translators
from cities import cities_json

texts = {
"Oceania": 'Oceania, the smallest continent, is made up of thousands of islands in the Pacific Ocean. It is home to a diverse range of cultures and landscapes, from the beaches of Australia to the volcanic islands of New Zealand. With a population of around 41 million, Oceania is known for its stunning natural beauty and unique wildlife.',
"Europe": 'Europe is the second smallest continent, but it is the most densely populated. It is home to over 740 million people and is known for its rich history, diverse cultures, and stunning architecture. From the rolling hills of Tuscany to the bustling cities of London and Paris, Europe offers a wide range of experiences for travelers.',
"Antarctica": 'Antarctica is the coldest and driest continent on Earth, and it is the only one without a permanent population. It is home to a small number of researchers and scientists who study the unique environment and wildlife of the continent. Despite its harsh conditions, Antarctica is a place of great natural beauty and scientific importance.',
"South America": 'South America is the fourth largest continent and is known for its diverse landscapes, from the Amazon rainforest to the Andes mountains. With a population of over 430 million, South America is home to a rich tapestry of cultures and traditions. It is also known for its vibrant music and dance, such as the samba and tango.',
"North America": 'North America is the third largest continent and is home to over 580 million people. It is known for its diverse landscapes, from the rocky mountains of Canada to the beaches of Mexico. North America is also home to some of the world''s largest and most influential cities, such as New York and Los Angeles.',
"Africa": 'Africa is the second largest continent and is home to over 1.2 billion people. It is known for its stunning wildlife, diverse cultures, and rich history. From the Sahara Desert to the savannas of the Serengeti, Africa offers a wide range of experiences for travelers.',
"Asia": 'Asia is the largest continent and is home to over 4.6 billion people. It is known for its diverse cultures, stunning landscapes, and rich history. From the bustling cities of Tokyo and Shanghai to the ancient temples of Angkor Wat, Asia offers a wide range of experiences for travelers.',
"Subscribe": 'If you enjoyed this video, make sure to give it a thumbs up and subscribe to our channel for more content like this. We''d love to hear from you in the comments section - let us know which countries, provinces, cities, rivers, seas, lakes, mountains, deserts, or any other places you''d like to see more videos about. Your feedback helps us create content that you''ll love! Thanks for watching!',
}

texts = {
            "Oceania": "Oceania is the smallest continent, made up of many islands in the Pacific Ocean. It has around 41 million people and is famous for its beautiful nature and unique animals.",
            "Europe": "Europe is the second smallest continent, but it has the most people, with over 740 million. It has a rich history, different cultures, and amazing buildings. You can see rolling hills in Tuscany and busy cities like London and Paris.",
            "Antarctica": "Antarctica is the coldest and driest continent, and no one lives there permanently. Only a few scientists study the environment and animals. Even though it's tough, Antarctica is very beautiful and important for science.",
            "South America": "South America is the fourth largest continent and has over 430 million people. It has different landscapes, like the Amazon rainforest and the Andes mountains. South America is also famous for its lively music and dances.",
            "North America": "North America is the third largest continent and has over 580 million people. It has diverse landscapes, from the rocky mountains in Canada to the beaches in Mexico. Some of the world's biggest and most important cities, like New York and Los Angeles, are in North America.",
            "Africa": "Africa is the second largest continent and has over 1.2 billion people. It's known for its amazing animals, different cultures, and rich history. You can see the Sahara Desert and the Serengeti savannas in Africa.",
            "Asia": "Asia is the biggest continent and has over 4.6 billion people. It's famous for its different cultures, beautiful landscapes, and rich history. You can visit busy cities like Tokyo and Shanghai or ancient temples like Angkor Wat in Asia.",
            "Subscribe": 'If you enjoyed this video, make sure to give it a thumbs up and subscribe to our channel for more content like this. We''d love to hear from you in the comments section - let us know which countries, provinces, cities, rivers, seas, lakes, mountains, deserts, or any other places you''d like to see more videos about. Your feedback helps us create content that you''ll love! Thanks for watching!',
        }

texts = {
    "Arctic Ocean": "The Arctic Ocean is the smallest and shallowest ocean. It is located in the icy north, between northern North America and Eurasia. Some people consider it a part of the Atlantic Ocean. The Arctic Ocean has an average depth of 1205 meters and a coastline of 45389 kilometers.",
    "Southern Ocean": "The Southern Ocean is the youngest of the five oceans and surrounds the continent of Antarctica. It is sometimes considered an extension of the Pacific, Atlantic, and Indian Oceans. The Southern Ocean has an average depth of 3270 meters and a coastline of 17968 kilometers.",
    "Indian Ocean": "The Indian Ocean is the warmest ocean and is located between southern Asia, Africa, and Australia. It has an average depth of 3741 meters and a coastline of 66526 kilometers. The Indian Ocean is known for its beautiful coral reefs and diverse marine life.",
    "Atlantic Ocean": "The Atlantic Ocean is the second largest ocean and is situated between the Americas to the west and Europe and Africa to the east. It has an average depth of 3646 meters and a coastline of 111866 kilometers. The Atlantic Ocean is famous for its powerful ocean currents and rich marine biodiversity.",
    "Pacific Ocean": "The Pacific Ocean is the largest and deepest ocean. It is located between Asia and Australasia to the west and the Americas to the east. The Pacific Ocean has an average depth of 3970 meters and a coastline of 135663 kilometers. It is known for its stunning coral reefs, diverse marine life, and numerous islands."
}


def test_records():
    # Query the devices
    devices = sd.query_devices()
    for device in devices:
        print(device["index"], device["name"], device["max_input_channels"])

    # Get the index of the virtual microphone
    device_index = None
    for device in sd.query_devices():
        if 'Virtual Cable' in device['name']:
            device_index = device['index']
            break

    if device_index is None:
        print('Virtual microphone not found')
    else:
        fs = 44100  # Sample rate
        seconds = 20  # Duration of recording

        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, device=device_index)
        sd.wait()  # Wait until recording is finished
        write('output.wav', fs, myrecording)  # Save as WAV file

        sound = AudioSegment.from_wav('output.wav')
        sound.export('output.mp3', format='mp3')

    return


#test_records()

time.sleep(10)

#file_name = 'c:\Cache\Sounds\en\db3bb522ccb7a2a693233feb7dd1071c.mp3'
#SoundHelper.remove_silence(file_name, file_name.replace('.mp3', '_out.mp3'))

def translate_and_pronounce(texts, override=False):
    for lang in used_langs:  # ["en", "ko"]
        translator = global_translators[lang]
        tts = TextToSpeechHelper(lang)
        tts.activate_window()
        tts.select_language(lang)
        tts.return_to_text()

        for k, text in texts.items():
            translation = text if lang == "en" else translator.translate(text)
            print(translation)
            seconds = TextToSpeechHelper.get_max_expected_recording_time(lang, translation)
            file_name = SoundHelper.get_filename_for(lang, translation)
            if override:
                os.path.re
            if os.path.exists(file_name):
                print(f'{file_name} already recorded')
                continue
            recorder = AudioRecorder(seconds, file_name)
            recorder.start_recording()
            tts.pronounce(translation)
            recorder.stop_recording()
            print(f'{file_name} recorded')
            SoundHelper.remove_silence(file_name)

def pronounce(translated_texts):
    for lang in used_langs:  # ["en", "ko"]
        translator = global_translators[lang]
        tts = TextToSpeechHelper(lang)
        tts.activate_window()
        tts.select_language(lang)
        tts.return_to_text()
        cl = translated_texts[lang]

        for c in cl:
            text = cl[c]
            print(text)
            translation = text #if lang == "en" else translator.translate(text)
            print(translation)
            seconds = TextToSpeechHelper.get_max_expected_recording_time(lang, translation)
            file_name = SoundHelper.get_filename_for(lang, translation)
            if os.path.exists(file_name):
                print(f'{file_name} already recorded')
                continue
            recorder = AudioRecorder(seconds, file_name)
            recorder.start_recording()
            tts.pronounce(translation)
            recorder.stop_recording()
            print(f'{file_name} recorded')
            SoundHelper.remove_silence(file_name)
            del recorder

def pronounce_groupped(translated_texts):
    portion = 25
    for lang in used_langs:  # ["en", "ko"]
        translator = global_translators[lang]
        tts = TextToSpeechHelper(lang)
        tts.activate_window()
        tts.select_language(lang)
        tts.return_to_text()
        cl = translated_texts[lang]
        group = []

        for c in cl:
            text = cl[c]
            if text is None or text == '':
                continue
            #print(text)
            translation = text #if lang == "en" else translator.translate(text)
            print(translation)
            file_name = SoundHelper.get_filename_for(lang, translation)
            if os.path.exists(file_name):
                print(f'{file_name} already recorded')
                continue
            group.append((file_name, translation))
            if len(group) == portion:
                pronounce_group(group, tts, lang)
                group = []
                #break

        if len(group) > 0:
            pronounce_group( group, tts, lang)

def change_file_extension(filename, new_extension):
    base_name = os.path.splitext(filename)[0]
    new_filename = base_name + '.' + new_extension
    return new_filename

def extract_fragment(audio_file, file_name, start, end):
    # Load MP3 file
    sound = AudioSegment.from_mp3(audio_file)

    # Slice the audio from start to end seconds
    sliced_audio = sound[start*1000:end*1000]

    # Save the sliced audio to the output file
    sliced_audio.export(file_name, format="mp3")



def split_into_sentenses(group, audio_file):
    for file_name, translation in group:
        print(f'("{file_name}", "{translation}"),')
    pass

    #wav = change_file_extension(audio_file, "wav")
    #audio.write_audiofile(wav)
    #sampling_rate, data = wavfile.read(wav)

    # Load the audio file
    y, sr = librosa.load(audio_file)

    # Define the hop length (in samples)
    step = 0.05
    hop_length = int(sr * step)

    # Initialize an empty list to store the results
    results = []

    sounds = []
    sound_db = 25 #39 if lang == "en" else 43 if lang == "ru" else 39 if lang == "ja" else 39

    # Process the audio in 0.1 seconds intervals
    for i in range(0, len(y) - 1, hop_length):
        # Extract the 0.1 seconds interval
        y_interval = y[i:i + hop_length]

        # Compute the spectrogram
        D = librosa.stft(y_interval)

        # Convert to dB scale
        D_db = librosa.amplitude_to_db(abs(D), ref=np.max)
        avg_db = abs(np.mean(D_db))

        # Check if there is sound in the interval
        sounds.append((round(i / sr, 2), abs(avg_db) > sound_db))

    timing_db = pd.DataFrame(columns=["timing", "db"], data=sounds)
    w = 25
    #last_row = timing_db[timing_db['timing'] == timing_db['timing'].max()]
    #max_t = timing_db['timing'].max()
    #for i in range(w):
        #r = last_row.copy()
        #max_t += step
        #r['timing'] = max_t
        #timing_db.loc[len(timing_db.index)] = r

    timing_db['rollingsum20'] = timing_db['db'].rolling(window=w).sum()
    timing_db.fillna(0.0, inplace=True)
    timing_db0 = timing_db.copy()
    timing_db.loc[timing_db['rollingsum20'] <= 3, 'rollingsum20'] = 0.0
    timing_db.loc[timing_db['rollingsum20'] > 0, 'rollingsum20'] = 1.0


    intervals = []
    start = None

    for idx, row in timing_db.iterrows():
        if row['rollingsum20'] == 1 and start is None:
            start = row['timing']
        elif row['rollingsum20'] == 0 and start is not None:
            end = row['timing']
            if end - start < 0.3:
                print(start, end)
            if end - start >= 0.3:
                intervals.append((start, end))
            start = None
    end = row['timing']
    if end is not None and start is not None and end - start >= 0.3:
        intervals.append((start, end))
    # Print the intervals
    for interval in intervals:
        print(f"Start: {interval[0]}, End: {interval[1]}")

    pre_look = (1.5 / 0.05 * step)
    if len(group) == len(intervals):
        for i in range(len(group)):
            file_name = group[i][0]
            interval = intervals[i]
            slice = timing_db[(timing_db["timing"] >= interval[0] - pre_look) & (timing_db["timing"] < interval[1])]
            sounds = slice.loc[slice['db']]
            if len(sounds) > 0:
                start_interval = round(slice.loc[sounds.index[0]]["timing"] - 0.1, 2)
                end_interval = round(slice.loc[sounds.index[-1]]["timing"] + 0.4, 2)
                if end_interval > max(timing_db["timing"]):
                    end_interval = max(timing_db["timing"])
                print(f'{{"phrase": "{group[i][1]}", "start": {start_interval}, "end": {end_interval}}},')
                extract_fragment(audio_file, file_name, start_interval, end_interval)
    pass
    print(1)
    """
    # Set the figure size (width, height)
    plt.figure(figsize=(40, 2))

    # Plot 'rollingsum20' against 'timing'
    plt.plot(timing_db['timing'], timing_db['rollingsum20'])

    # Save the figure to a file
    plt.savefig(self.change_file_extension(audio_file, "png"), dpi=300)

    # Show the plot
    #plt.show()

    pre_look = (1.5 / 0.05 * step)
    zipped = zip(intervals, sentences)
    for interval, country in zipped:
        slice = timing_db[(timing_db["timing"] >= interval[0]-pre_look) & (timing_db["timing"] < interval[1])]
        sounds = slice.loc[slice['db']]
        if len(sounds) > 0:
            start_interval = round(slice.loc[sounds.index[0]]["timing"]-0.1, 2)
            end_interval = round(slice.loc[sounds.index[-1]]["timing"]+0.4, 2)
            print(f'{{"phrase": "{country}", "file": "{audio_file}", "start": {start_interval}, "end": {end_interval}}},')

    print(f'done {len(intervals)} detected')
    print(f'done {len(intervals)} detected')
    """

def pronounce_group(group, tts, lang):
    random.shuffle(group)
    s = ""
    tmp_file_name = "output.mp3"
    for file_name, translation in group:
        s = s + f'<s>{translation}</s> <break time="2000ms"/>'

    s = "<speak>" + s + "</speak>"

    seconds = 60 + len(group) * 5
    recorder = AudioRecorder(seconds, tmp_file_name)
    recorder.start_recording()
    tts.pronounce(s)
    recorder.stop_recording()
    print(f'{tmp_file_name} recorded')
    SoundHelper.remove_silence(tmp_file_name, 5.0)
    split_into_sentenses(group, tmp_file_name)
    del recorder


group = [
    ("c:/Cache/Sounds/ru/1ad84beab2666ca9ae4bcfbfbc39783b.mp3", "Андорра"),
    ("c:/Cache/Sounds/ru/13d929bd32656a2271888fd73d625adc.mp3", "Франция"),
    ("c:/Cache/Sounds/ru/f45077285ac1486668724e5ec4a16559.mp3", "Словакия"),
    ("c:/Cache/Sounds/ru/b03cff4b5334a8e80be847d99f4a3a43.mp3", "Австрия"),
    ("c:/Cache/Sounds/ru/e5e20d4a8fa25b7aaca4ee4342f238a9.mp3", "Венгрия"),
]
#split_into_sentenses(group, 'output.mp3')
#pronounce_groupped(countries.countries)
#pronounce(countries.countries)
translate_and_pronounce(texts)
#pronounce_groupped(cities_json)
#pronounce(cities_json)



