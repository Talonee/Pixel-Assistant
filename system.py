
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import numpy as np 
from scipy.optimize import curve_fit   
from matplotlib import pyplot as plt

import numpy
from sympy import S, symbols, printing
import matplotlib.pyplot as plt
import time
import os

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

class Audio():
    def __init__(self):
        self.convert = {
            "100": 0.0,
            "95": -0.77,
            "90": -1.59,
            "85": -2.46,
            "80": -3.38,
            "75": -4.36,
            "70": -5.41,
            "65": -6.53,
            "60": -7.75,
            "55": -9.06,
            "50": -10.50,
            "45": -12.10,
            "40": -13.88,
            "35": -15.90,
            "30": -18.23,
            "25": -20.98,
            "20": -24.34,
            "15": -28.67,
            "10": -34.74,
            "5": -44.99,
            "0": -95.25
        }

    def setVolume(self, level):
        rem = level % 10
        level //= 10
        if 0 <= rem <= 2: # round down
            res = level * 10
        elif 3 <= rem <= 7: # endings in 5
            res = level * 10 + 5
        elif 8 <= rem: # round up
            res = (level + 1) * 10
        audioValue = str(res)
        volume.SetMasterVolumeLevel(self.convert[audioValue], None)

    def getVolume(self):
        return volume.GetMasterVolumeLevel()

# pass speak and getaudio into this somehow
class Window():
    def __init__(self):
        pass

    def sleep():
        speak("Do you wish to sleep?") 
        sleep = getaudio()
        if sleep == 'no': 
            exit() 
        else: 
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    def shutdown(self):
        speak("Do you wish to shutdown your computer?") 
        shutdown = getaudio()
        if shutdown == 'no': 
            exit() 
        else: 
            os.system("shutdown /s /t 1") 

    def restart(self):
        speak("Do you wish to restart your computer?") 
        restart = getaudio()
        if restart == 'no': 
            exit() 
        else: 
            os.system("shutdown /r /t 1") 

class Screen():
    def __init__(self):
        pass

    def setBrightness(self, level):
            # num = [i for i in list(text) if i.isdigit()]
            # brightness = int("".join(num))
            # wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness, 0)
            wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(level, 0)





# audio = Audio()
# audio.setVolume(79)
# print(audio.getVolume())


# stacked_x = numpy.array([x,x+1,x-1])
# coeffs = mpf(stacked_x, y, deg) 


# plt.plot(x_first, y_first, 'o')
# coeffs = numpy.polyfit(x_first,y_first,1)
# x2 = numpy.arange(min(x_first)-1, max(x_first)+1, 0.01) #use more points for a smoother plot
# y2 = numpy.polyval(coeffs, x2) #Evaluates the polynomial for each x2 value
# plt.plot(x2, y2, label="deg=3")
# plt.legend()
# plt.show()

# print(coeffs)
# x = symbols("x")
# poly = sum(S("{:6.2f}".format(v))*x**i for i, v in enumerate(coeffs[::-1]))
# eq_latex = printing.latex(poly)
# print(eq_latex)



# a = coeffs[0]
# b = coeffs[1]
# c = coeffs[2]
# d = coeffs[3]
# e = coeffs[4]
# f = coeffs[5]
# model = lambda x: a*(x**5) + b*(x**4) + c*(x**3) + d*(x**2) + e*x+f

# def polynomial(coeffs, index, degree):
#     if degree == 0:
#         return str(coeffs[index])
#     # return str(coeffs[index], **degree + polynomial(coeffs, index + 1, degree - 1)
#     return f"{coeffs[index]:.2f}x^{degree} " + polynomial(coeffs, index + 1, degree - 1)
# print(coeffs)
# print(polynomial(coeffs, 0, 5))

# for i in np.arange(0, 1.05, 0.05):
# for i in np.arange(0, 1.05, 0.05):
#     print(f"{(i * 100):.0f}% has a value of {model(i):.2f}")
#     volume.SetMasterVolumeLevel(model(i), None)
#     time.sleep(1)


# print(volume.GetMute())
# volume.GetMasterVolumeLevel()
print(volume.GetMasterVolumeLevel())
# print(volume.GetVolumeRange())
# # volume.SetMasterVolumeLevel(-20.0, None)
# for i in range(1, 20):
#     print(volume.GetMasterVolumeLevel())
#     volume.SetMasterVolumeLevel(-0.8*i, None)
#     time.sleep(1)
    # volume.SetMasterVolumeLevel(-1.6, None)
    # time.sleep(2)
    # volume.SetMasterVolumeLevel(-2.4, None)
    # time.sleep(2)












# VOL = -0.7781546711921692
# for i in range(1,8):
#     print(f"Iteration {i}: {i * VOL}")
# minVolume = volume.GetVolumeRange()[0]
# maxVolume = volume.GetVolumeRange()[1]
# incVolume = volume.GetVolumeRange()[2]
# n = (maxVolume - minVolume) / incVolume
# print(minVolume, maxVolume, n)
# for i in range(int(n)):
#     print(f"Vol: {minVolume + i * incVolume}")
#     volume.SetMasterVolumeLevel(minVolume + i * incVolume, None)
#     time.sleep(0.1)

# volume.SetMasterVolumeLevel(-60, None)
# print(volume.GetMasterVolumeLevel())

# volRange = minVolume - maxVolume 

# def setVolume(perc):
#     vol = minVolume - volRange * perc / 100 
#     print(vol)
#     volume.SetMasterVolumeLevel(vol, None)

# setVolume(20)
