# overlapping notes

from scipy.io.wavfile import write
from numpy import linspace, sin, pi, int16, exp, zeros
from pylab import plot, show, axis
import numpy as np
import csv

totalLength = 22 #seconds
sampleRate = 4000 # points per second

T = linspace(0,totalLength,totalLength*sampleRate)  #time coordinates of sample points
music = zeros(len(T))

# Apply ADSR envelope on on the note
def piecewise_linear_envelope(A, D, S, R, maxlevel, time, len):
    if time < A:
        return maxlevel * time / A
    elif time < A + D:
        return(maxlevel - (time - A) * (maxlevel - S) / D)
    elif time > len - R:
        return S - (time - (len - R)) * S / R
    else:
        return S


def piecewise_exp_envelope(A, D, S, R, maxlevel, time, len):
    if time <= A:
        timeconstant = A/5 ;
        return maxlevel * (1- exp(-time/timeconstant))
    elif time < A + D:
        timeconstant = D /5;

        C2 = (maxlevel-S)*exp(A/timeconstant)/(1 - exp(-D/timeconstant))
        C1 = (S - maxlevel*exp(-D/timeconstant))/(1 - exp(-D/timeconstant))
        return C1 + C2*exp(-time/timeconstant)
    elif time > len - R:
        timeconstant = R / 5;
        start_release = len - R
        C2 = S * exp( (len-R) / timeconstant) / (1 - exp(-R / timeconstant))
        C1 = ( -S * exp(-R / timeconstant)) / (1 - exp(-R / timeconstant))
        return C1 + C2 * exp(-time / timeconstant)
    else:
        return S


def ADSR(data, len, rate, a=0.1, d=0.5, S=0, r=0.0, maxlevel=1):
    A = len*a
    D = len*d
    R = len*r
    t = linspace(0, len, len * sampleRate)
    #data = data envelope(A,D,S,R,maxlevel,t,len);
    for i in range(int(len*rate)):
        data[i] = data[i]*piecewise_exp_envelope(A,D,S,R,maxlevel,t[i],len);
    return data




def addnote(hz,start,duration, weight=1):
    t = linspace(0,duration,duration*sampleRate)
    a = np.sin(2*np.pi*hz*t)*weight
    a = ADSR(a, duration, sampleRate)
    startPoint = int(start*sampleRate)
    endPoint = startPoint + len(t)
    music[startPoint:endPoint] += a

with open('interstellar3.csv', ) as f:
    reader = csv.reader(f, delimiter=',', quotechar='|')
    for row in reader:
        addnote(float(row[0]), float(row[1])/700, float(row[2])/200)
        #addnote(float(row[0])*2, float(row[1]) /700, float(row[2]) /400)
        #print float(row[1])
        #print float(row[1])/1000
        #.append([float(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])])
        #duration.append(float(row[6]))


#addnote(523, 0, 1.5, 2)
#addnote(659 ,0,1.5)
#addnote(1047 ,0,1.5)
write('music5.wav', sampleRate, music)  # writing the sound to a file
plot(T,music)
show()