from gtts import gTTS
import os

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
    tts = Speaker('en')
    tts.speak(s)  # Output the string variable to speaker

