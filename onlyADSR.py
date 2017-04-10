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
        return  maxlevel * (1- exp(-time/timeconstant)) # for piano and violin  maxlevel * time / A#
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
        return C1 + C2 * exp(-time / timeconstant)# for flute maxlevel*(1-exp(-(float(len)- time)/timeconstant))#
    else:
        return S


# for piano a=0.05, d=0.3, S=0.25, r=0.6
# for guitar  a=0.001, d=0.5, S=0.0, r=0.0
# for violin a=0.2, d=0.0, S=1, r=0.0
# for flute a=0.25, d=-0.0, S=1, r=0.3
def ADSR(data, len, rate,a=0.2, d=0.3, S=1, r=0.3, maxlevel=1):
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
 data = sin(2*pi*freq*t)*amp #for guitar + sin(2*pi*freq*t)*amp/2 + sin(3*pi*freq*t)*amp/3 + sin(4*pi*freq*t)*amp/6
 data = ADSR(data,len,rate)
 return data.astype(int16) # two byte integers


# A tone, 2 seconds, 44100 samples per second
tone = note(392.00, 3, amp=10000)

write('temp.wav',44100,tone) # writing the sound to a file

plot(linspace(0,3,3*44100),tone)
axis([0,3,15000,-15000])
show()