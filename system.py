
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



# pass speak and getaudio into this somehow



class Audio():
    def __init__(self):
        # scale = {'100%': 0, '99%': -0.15066957473754883, '98%': -0.30284759402275085, '97%': -0.4565645754337311, '96%': -0.6118528842926025, '95%': -0.768743097782135,
        #        '94%': -0.9272695183753967, '93%': -1.0874667167663574, '92%': -1.2493702173233032, '91%': -1.4130167961120605, '90%': -1.5784454345703125,
        #        '89%': -1.7456932067871094, '88%': -1.9148017168045044, '87%': -2.08581280708313, '86%': -2.2587697505950928, '85%': -2.4337174892425537,
        #        '84%': -2.610703229904175, '83%': -2.7897727489471436, '82%': -2.970977306365967, '81%': -3.1543679237365723, '80%': -3.339998245239258,
        #        '79%': -3.527923583984375, '78%': -3.718202590942383, '77%': -3.9108924865722656, '76%': -4.1060566902160645, '75%': -4.3037590980529785,
        #        '74%': -4.5040669441223145, '73%': -4.707049369812012, '72%': -4.912779808044434, '71%': -5.121333599090576, '70%': -5.33278751373291,
        #        '69%': -5.547224998474121, '68%': -5.764730453491211, '67%': -5.98539400100708, '66%': -6.209307670593262, '65%': -6.436570644378662,
        #        '64%': -6.6672821044921875, '63%': -6.901548862457275, '62%': -7.1394829750061035, '61%': -7.381200790405273, '60%': -7.626824855804443,
        #        '59%': -7.876484394073486, '58%': -8.130311965942383, '57%': -8.388449668884277, '56%': -8.651047706604004, '55%': -8.918261528015137,
        #        '54%': -9.190258026123047, '53%': -9.46721076965332, '52%': -9.749302864074707, '51%': -10.036728858947754, '50%': -10.329694747924805,
        #        '49%': -10.62841796875, '48%': -10.933131217956543, '47%': -11.2440767288208, '46%': -11.561516761779785, '45%': -11.88572883605957,
        #        '44%': -12.217005729675293, '43%': -12.555663108825684, '42%': -12.902039527893066, '41%': -13.256492614746094, '40%': -13.61940860748291,
        #        '39%': -13.991202354431152, '38%': -14.372318267822266, '37%': -14.763236045837402, '36%': -15.164472579956055, '35%': -15.576590538024902,
        #        '34%': -16.000192642211914, '33%': -16.435937881469727, '32%': -16.884546279907227, '31%': -17.3467960357666, '30%': -17.82354736328125,
        #        '29%': -18.315736770629883, '28%': -18.824398040771484, '27%': -19.350669860839844, '26%': -19.895822525024414, '25%': -20.461252212524414,
        #        '24%': -21.048532485961914, '23%': -21.6594181060791, '22%': -22.295886993408203, '21%': -22.960174560546875, '20%': -23.654823303222656,
        #        '19%': -24.38274574279785, '18%': -25.147287368774414, '17%': -25.95233154296875, '16%': -26.80240821838379, '15%': -27.70285415649414,
        #        '14%': -28.66002082824707, '13%': -29.681535720825195, '12%': -30.77667808532715, '11%': -31.956890106201172, '10%': -33.23651123046875,
        #        '9%': -34.63383865356445, '8%': -36.17274856567383, '7%': -37.88519287109375, '6%': -39.81534194946289, '5%': -42.026729583740234,
        #        '4%': -44.61552047729492, '3%': -47.73759078979492, '2%': -51.671180725097656, '1%': -56.992191314697266, '0%': -65.25}

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Set volume to a specified level
    def setVolume(self, level):
        # Remove % and set level to between 0 and 1
        level = (int(level.replace("%", "")) if "%" in level else int(level)) / 100
        
        # Cap volume level if exceed 100% or below 0%
        level = 1 if level > 1 else 0 if level < 0 else level 

        self.volume.SetMasterVolumeLevelScalar(level, None)

    # Get current volume level
    def getVolume(self):
        return f"{self.volume.GetMasterVolumeLevelScalar() * 100:.0f}" + "%"
    
    # Increase volume by/to a specified level
    def increaseVolume(self, pre="by", level="10"):
        # Remove % and set increment to between 0 and 1
        level = (int(level.replace("%", "")) if "%" in level else int(level)) / 100
        curr = round(self.getVolume(), 2)

        if pre == "by":
            level = curr + level
        elif pre == "to":
            level = abs(level)

        level = 0 if level < 0 else 1 if level > 1 else level

        self.volume.SetMasterVolumeLevelScalar(level, None)

    # Decrease volume by/to a specified level
    def decreaseVolume(self, pre="by", level="10"):
        # Remove % and set increment to between 0 and 1
        level = (int(level.replace("%", "")) if "%" in level else int(level)) / 100
        curr = round(self.getVolume(), 2)

        if pre == "by":
            level = curr - level
        elif pre == "to":
            level = abs(level)

        level = 0 if level < 0 else 1 if level > 1 else level

        self.volume.SetMasterVolumeLevelScalar(level, None)

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





audio = Audio()
print(audio.getVolume())
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
# print(volume.GetMasterVolumeLevel())
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
