from piper import PiperVoice
import sounddevice as sd
import numpy as np
import sys

import re

from confighandle import CONFIG

class TTS:
    def __inti__(self):
        self.tts_model = CONFIG["TTS"]["model"]
        self.voice: PiperVoice 
        
    def LoadTTSModle(self,model_path,model_config_path=None):
        print("\nloading TTS")
        try:
            self.voice = PiperVoice.load(model_path=model_path,config_path=model_config_path)
            print(f"TTS Loaded\nModel path:{model_path}")
        except SystemError as Error:
            print("Error! Can't Load TTS")
            print(Error)
            sys.exit(1)
        
    @staticmethod
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


    def speak(self,text: str):
        try:
            text = self.clear_text(text)
            stream = sd.OutputStream(samplerate=self.voice.config.sample_rate, channels=1, dtype='int16')
            stream.start()

            for audio_bytes in self.voice.synthesize(text):
                int_data = np.frombuffer(audio_bytes.audio_int16_bytes, dtype=np.int16)
                stream.write(int_data)

            stream.stop()
            stream.close()
        except SystemError as Error:
            print("Error! TTS Can't Speak")
            print(Error)








# testing code
if __name__ == "__main__":
    tts = TTS()
    tts.LoadTTSModle(CONFIG["TTS"]["model"])
    tts.speak("Hello!")