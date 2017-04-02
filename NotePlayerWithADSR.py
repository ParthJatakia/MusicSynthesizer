from scipy.io.wavfile import write
from numpy import linspace, sin, pi, int16, exp
from pylab import plot, show, axis
import numpy as np
import csv

freq = []
duration = []
with open('music.csv', ) as f:
    reader = csv.reader(f, delimiter=',', quotechar='|')
    for row in reader:
        freq.append(float(row[0]))
        duration.append(float(row[1]))

length = 0
for i in duration:
    length = length + (i/1000)

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

def ADSR(data, len, rate, a=0.15, d=0.85, S=0.0, r=0.0, maxlevel=1):
    A = len*a
    D = len*d
    R = len*r
    t = linspace(0, len, len * rate)
    #data = data envelope(A,D,S,R,maxlevel,t,len);
    for i in range(int(len*rate)):
        data[i] = data[i]*piecewise_linear_envelope(A,D,S,R,maxlevel,t[i],len);
    return data

# tone synthesis
def note(freq, len, amp=5000, rate=44100):
 t = linspace(0,len,len*rate)
 data = sin(2*pi*freq*t)*amp
 data = ADSR(data,len,int(rate))
 return data.astype(int16)


def stitch():
    data = np.empty(shape=(0, 0))
    for i in range(0, len(duration)-1):
        lenNote = duration[i]/1000
        data = np.append(data, note(freq[i], lenNote))
        print(i)
    return data.astype(int16)

# A tone, 2 seconds, 44100 samples per second
tone = stitch()
print(tone.shape)
write('titanic85_lin.wav', 44100, tone)  # writing the sound to a file
toplot = tone.tolist()
print(length)
plot(linspace(0, length, len(toplot)), toplot)
axis([0, 0.4, 15000, -15000])
show()
