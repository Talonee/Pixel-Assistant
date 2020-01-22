# Google Calendar
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS

import wmi # control brightness
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


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

def run(here):
    if here < 5:
        speak("I'm a boat")
        return "Still going"
    else:
        return "I'm done"

# speak("Hello, what would you like me to do?")
# get_audio()

# text = get_audio()
# if "hello" in text:
#     speak("Hey wassup man?")

# if "your name" in text:
#     speak("My name is Pixel.")

# if "change brightness" in text or "lower brightness" in text:
#     num = [i for i in list(text) if i.isdigit()]
#     brightness = int("".join(num))
#     wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness, 0)

# if "hi to my" in text:
#     target = text.split(" ")
#     speak(f"Hello, Talon's {target[-1]}")


# if __name__ == "__main__":
#     with open("key.json") as f:
#         key = json.load(f)
#         print(key["ID"])



def authenticate_google():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_events(n, service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])




service = authenticate_google()
get_events(2, service)

# if __name__ == '__main__':
#     main()