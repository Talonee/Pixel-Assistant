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
import pyttsx3
import speech_recognition as sr
import pytz
import subprocess

import json


import system

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")
    engine.setProperty('rate', 175)
    engine.say(text)
    engine.runAndWait()


def get_audio():
    # print("Ready to listen...")
    r = sr.Recognizer()
    with sr.Microphone(1) as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception" + str(e))
    
    # speak("Yes")
    print("Ready to listen...")
            
    return said.lower()


# speak("Hello, what would you like me to do?")
# get_audio()

# text = get_audio()
# if "hello" in text:
#     speak("Hey wassup man?")

# if "your name" in text:
#     speak("My name is Pixel.")

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

def get_events(day, service):
    # Call the Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone()
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day.")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "AM"
            else:
                start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
                start_time = start_time + "PM"

            speak(event["summary"] + " at " + start_time)


def get_date(text):
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year += 1
    
    if day < today.day and month == -1 and day != -1:
        month += 1

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") > 0:
                dif += 7 
        
        return today + datetime.timedelta(dif)

    if month == -1 or day == -1:
        return None

    return datetime.date(month=month, day=day, year=year)

# def set_master_volume(vol):
#     pass

# set_master_volume(40)

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    vsc = "C:/Users/Cakee/AppData/Local/Programs/Microsoft VS Code/Code.exe"
    notepad = "C:/WINDOWS/system32/notepad.exe"
    subprocess.Popen([notepad, file_name])


WAKE = "serena"
SERVICE = authenticate_google()



listen = True
while listen:
    print("Initiate... Listening")
    text = get_audio()
    if text.count(WAKE) > 0:
        text = get_audio()

        CALENDAR_STRS = ["today", "plan", "planned", "plans",
                            "am i busy", "what do i have"]
        for phrase in CALENDAR_STRS:
            if phrase in text:
                date = get_date(text)
                if date:
                    get_events(get_date(text), SERVICE)
                else:
                    speak("I don't understand.")
                break

        NOTE_STRS = ["make a note", "write this down", "remind me", "listen to me"]
        for phrase in NOTE_STRS:
            if phrase in text:
                speak("What would you like me to write down?")
                txt = get_audio()
                note(txt)
                speak("I have just made a note.")
                break

        if "change brightness" in text or "lower brightness" in text:
            # Run system.screen.setBrightness()
            # num = [i for i in list(text) if i.isdigit()]
            # brightness = int("".join(num))
            # wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness, 0)
            pass


        COM_STATUS = ["sleep", "restart", "turn off", "shut down"]
        for phrase in COM_STATUS:
            if phrase in text:
                if "set to" in text:
                    response = "y"
                else:
                    speak(f"Do you want to {phrase}?")
                    response = get_audio()

                if response[0] == "y":
                    if "sleep" in phrase:
                        print("Attempting to sleep...")
                        system.Window().sleep()
                    elif "restart" in phrase:    
                        print("Attempting to restart...")
                        system.Window().restart()
                    elif "shut down" in phrase or "turn off" in phrase:
                        print("Attempting to shut down...")
                        system.Window().shutdown()

                    listen = False
                break
        

        VOLUME = ["change volume", "lower volume", "increase volume"]
        for phrase in VOLUME:
            if phrase in text:
                pass
                # Run system.audio.setVolume()
                # speak("Changing volume")
                # for word in text:
                #     if word.isdigit():
                #         print(f"Volume {word}")
                #         set_master_volume(int(word))
                #         break
                # break



# if __name__ == '__main__':