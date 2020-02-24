# This class handles simple computer settings

# Audio 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import os # Window
import wmi # Screen

class Audio():
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

    def setVolume(self, pre="to", level="10"):
        # Remove % and set level to between 0 and 1
        level = int(level) / 100

        if pre == "by":
            level = self._getVolume() + level
        else:
            level = abs(level)
        
        # Cap volume level if exceed 100% or below 0%
        level = 1 if level > 1 else 0 if level < 0 else level 

        self.volume.SetMasterVolumeLevelScalar(level, None)

    def toggleMute(self, status="mute"):
        val = 1 if status == "mute" else 0
        self.volume.SetMute(val, None)

    def getVolume(self):
        return f"{(self.volume.GetMasterVolumeLevelScalar() * 100):.0f}%"

    def _getVolume(self):
        return self.volume.GetMasterVolumeLevelScalar()

class Screen():
    def __init__(self):
        self.monitor = wmi.WMI(namespace='wmi')

    def setBrightness(self, pre="to", level="10"):
        # num = [i for i in list(text) if i.isdigit()]
        # brightness = int("".join(num))
        level = int(level)
        
        if pre == "by":
            level = self._getBrightness() + level
        else:
            level = abs(level)
        
        level = 0 if level < 0 else 100 if level > 100 else level

        self.monitor.WmiMonitorBrightnessMethods()[0].WmiSetBrightness(level, 0)

    def getBrightness(self):
        return f"{(self.monitor.WmiMonitorBrightness()[0].CurrentBrightness):.0f}%"

    def _getBrightness(self):
        return self.monitor.WmiMonitorBrightness()[0].CurrentBrightness

class Window():
    def __init__(self):
        pass

    def sleep():
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    def restart(self):
        os.system("shutdown /r /t 1")

    def shutdown(self):
        os.system("shutdown /s /t 1") 
 
audio = Audio()
# audio.setVolume(pre="by", level="-9%")
# audio.toggleMute()
# print(audio.muteVolume("on"))
# print(audio.getVolume())

screen = Screen()
# screen.setBrightness(pre="by", level="-91%")
# print(screen.getBrightness())