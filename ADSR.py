from scipy.io.wavfile import write
from numpy import linspace,sin,pi,int16,exp
from pylab import plot,show,axis


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

def ADSR(data, len, rate, a=0.01, d=0.99, S=0.0, r=0.0, maxlevel=1):
    A = len*a
    D = len*d
    R = len*r
    t = linspace(0, len, len * rate)
    #data = data envelope(A,D,S,R,maxlevel,t,len);
    for i in range(len*rate):
        data[i] = data[i]*piecewise_exp_envelope(A,D,S,R,maxlevel,t[i],len);
    return data

# tone synthesis
def note(freq, len, amp=9, rate=44100):
 t = linspace(0,len,len*rate)
 data = sin(2*pi*freq*t)*amp
 data = ADSR(data,len,rate)
 return data.astype(int16) # two byte integers


# A tone, 2 seconds, 44100 samples per second
tone = note(440,1,amp=10000)

write('piano.wav',44100,tone) # writing the sound to a file

plot(linspace(0,1,1*44100),tone)
axis([0,1,15000,-15000])
show()
