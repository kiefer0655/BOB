from piper import PiperVoice
import sounddevice as sd
import numpy as np

import re

from confighandle import CONFIG

tts_model = CONFIG["TTS"]["model"]

print("\nloading TTS")
voice = PiperVoice.load(tts_model)

print("TTS Loaded\n")

def clear_text(text):
    pattern = re.compile(
        r"[*"                              # match *
        r"\U0001F600-\U0001F64F"           # emoticons
        r"\U0001F300-\U0001F5FF"           # symbols & pictographs
        r"\U0001F680-\U0001F6FF"           # transport & map
        r"\U0001F1E0-\U0001F1FF"           # flags
        r"\U00002700-\U000027BF"
        r"\U0001F900-\U0001F9FF"
        r"\U00002600-\U000026FF"
        r"]+",
        flags=re.UNICODE
    )
    return pattern.sub("", text)


def speak(text: str):
    text = clear_text(text)
    stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16')
    stream.start()

    for audio_bytes in voice.synthesize(text):
        int_data = np.frombuffer(audio_bytes.audio_int16_bytes, dtype=np.int16)
        stream.write(int_data)

    stream.stop()
    stream.close()