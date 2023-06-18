from textblob import TextBlob
from gtts import gTTS
import os
import speech_recognition as sr
import wikipedia

def audio():
    r=sr.Recognizer()
    with sr.Microphone() as source:
         print("say somthing")
         audio=r.listen(source)
         data=r.recognize_google(audio, language="es")
         print(data)
         return data

def wiki():
    a=audio()

    blob = TextBlob(a)

    en = str(blob.translate(to='en'))

    result = wikipedia.summary(en, sentences = 2) 
    return result




def speak(a):
    tts = gTTS(text=a, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")


s=wiki()

blob = TextBlob(s)


print (blob.translate(to='es'))

hi = str(blob.translate(to='hi'))
es = str(blob.translate(to='es'))
speak(es + hi)

speak(s)
