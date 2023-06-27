from gtts import gTTS
import os
from multiprocessing import Process, Event
import time

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

def tts_thread(tts_Q, stop_event):
    tts = Speaker("en")
    while not stop_event.is_set():
        try:
            if not tts_Q.empty() :
                s = tts_Q.get()
                if isinstance(s, str) and s is not None:
                    tts.speak(s)
        except:
            continue

if __name__ == '__main__':
    s = "Please write in English language."  # The string variable
    tts_Q = Queue() 
    stop_event = Event()
    get_tts = threading.Thread(target=tts_thread, args=(tts_Q, stop_event))
    get_tts.start()
    tts_Q.put("Please write in English language." )
    while True:
        if tts_Q.empty() :
            tts_Q.put("test tts process")
        print("test tts Process")
        
        
    
