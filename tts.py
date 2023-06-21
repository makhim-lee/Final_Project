from gtts import gTTS
import os

def speak(text):
    tts = gTTS(text=text, lang='en')  # Convert text to speech
    filename = "speech.mp3"  # Name of mp3 file
    tts.save(filename)  # Save speech audio into a file
    os.system("mpg321 " + filename)  # Play the mp3 file


if __name__ == '__main__':
    s = "Please write in English language."  # The string variable
    speak(s)  # Output the string variable to speaker

