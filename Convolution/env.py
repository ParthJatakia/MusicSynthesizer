import numpy as np
from scipy.io import wavfile
from scipy import signal

inp = wavfile.read('interstellar16000PPS.wav')
rir = wavfile.read('Five_Columns_Long_16k.wav')

print(np.amax(inp[1]))

rir_left = rir[1][:, 0]
rir_right = rir[1][:, 1]

print(rir_left.size)
print(inp[1].size)

out_left = signal.fftconvolve(inp[1], rir_left)
out_right = signal.fftconvolve(inp[1], rir_right)

out_left = out_left * 10000 / np.max(np.abs(out_left))
out_right = out_right * 10000 / np.max(np.abs(out_right))

out = np.stack((out_left, out_right))
out = out.transpose()
out = np.asarray(out, dtype=np.int16)

wavfile.write('interstellar_five_column_long_echo.wav', 16000, out)
