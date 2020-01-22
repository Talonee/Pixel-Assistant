import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS

import wmi # control brightness

def speak(text):
    tts = gTTS(text=text, lang="en")
    fname = "voice.mp3"
    tts.save(fname)
    playsound.playsound(fname)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception" + str(e))
            
    return said


# speak("Hello, what would you like me to do?")
# get_audio()

text = get_audio()
if "hello" in text:
    speak("Hey wassup man?")

if "your name" in text:
    speak("My name is Pixel.")

if "change brightness" in text or "lower brightness" in text:
    num = [i for i in list(text) if i.isdigit()]
    brightness = int("".join(num))
    wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness, 0)


