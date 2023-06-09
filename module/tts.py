from gtts import gTTS
import os
from multiprocessing import Process, Event

import threading
from queue import Queue


class Speaker:
    def __init__(self, lang='en'):
        self.last_text = None
        self.lang = lang

    def speak(self, text):
        if text != self.last_text:
            tts = gTTS(text=text, lang='en')
            filename = "speech.mp3"
            tts.save(filename)
            os.system("mpg321 " + filename)
            self.last_text = text


if __name__ == '__main__':
    s = "Please write in English language."  # The string variable
    tts_Q = Queue()
    stop_event = Event()
    from process import tts_proc
    get_tts = threading.Thread(target=tts_proc, args=(tts_Q, stop_event))
    get_tts.start()
    tts_Q.put("Please write in English language.")
    while True:
        if tts_Q.empty():
            tts_Q.put("test tts process")
        print("test tts Process")
