import time
import sounddevice as sd
import numpy as np
import threading
import queue
from pydub import AudioSegment
from scipy.io.wavfile import write


class AudioRecorder:
    def __init__(self, seconds, output_file_name):
        self.output_file_name = output_file_name
        self.seconds = seconds
        self.q = queue.Queue()
        self.recording = False

        self.recording_thread = threading.Thread(target=self.record_audio, daemon=True)

        devices = sd.query_devices()
        #for device in devices:
        #    print(device["index"], device["name"], device["max_input_channels"])

        # Get the index of the virtual microphone
        self.device_index = None
        for device in sd.query_devices():
            if 'Virtual Cable' in device['name']:
                self.device_index = device['index']
                break

        if self.device_index is None:
            print('Virtual microphone not found')

        print(f"Default input device: {sd.default.device}")
        print(f"Default output device: {sd.default.device}")

    def record_audio(self):
        #with sd.InputStream(callback=self.queue_audio, samplerate=44100, blocksize=44100//2, device=self.device_index):
        #    #sd.default.device = AUDIO_DEVICE
        #    print("Starting recording...")
        #    while self.recording:
        #        time.sleep(0.1)
        fs = 44100
        self.myrecording = sd.rec(int(self.seconds * fs), samplerate=fs, channels=2, device=self.device_index)
        sd.wait()  # Wait until recording is finished
        write('output.wav', fs, self.myrecording)  # Save as WAV file

        sound = AudioSegment.from_wav('output.wav')
        sound.export(self.output_file_name, format='mp3')

    def queue_audio(self, indata, frames, time, status):
        #if status:
        print(f'status {status}')
        if self.recording:
            data = indata.copy()
            print(f'recorded {len(data)}')
            self.q.put(data)

    def start_recording(self):
        self.recording = True
        self.recording_thread.start()

    def stop_recording(self):
        self.recording = False
        self.recording_thread.join()
        #recorded_audio = []
        #while not self.q.empty():
        #    recorded_audio.append(self.q.get().copy())

        # Concatenate all blocks of audio data into a single array
        #recorded_audio = np.concatenate(recorded_audio)

        # Convert the recorded audio to an AudioSegment object
        #audio_segment = AudioSegment(recorded_audio.astype(np.int16).tobytes(),
        #                             frame_rate=44100, sample_width=2, channels=1)

        #audio_segment = AudioSegment(b''.join(recorded_audio), frame_rate=44100, sample_width=2, channels=1)

        # Export the AudioSegment object as an MP3 file
        #audio_segment.export("output.mp3", format="mp3")


