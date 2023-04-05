
import pandas as pd
from scipy.fft import fft
import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import write
import scipy.signal as signal

class GenWaveForm:

    def Sine(self, f, A, t):
        y = A*np.sin(2*np.pi*t*f)
        return y

    def Square(self, f, A, t):
        y = np.sign(A*np.sin(2*np.pi*t*f))
        return y

    def Sawtooth(self, f, A, t):
        y = A*signal.sawtooth(2*np.pi*f*t)
        return y

    def Triangle(self, f, A,t):
        y = signal.sawtooth(2*np.pi*f*t, 0.5)
        return y

    def WhiteNoise(self, A,t):
        y = A*np.random.rand(len(t))
        return y

    def DrawProc(self, y, lim, name):
        plt.plot(self.t, y)
        plt.xlim(left = 0, right = lim)
        plt.title("Waveform: %s"%name)
        plt.xlabel("t[s]")
        plt.ylabel("y: %s"%name)
        plt.show()

    def TransformataFouriera(self, y, t):
        N = len(t)
        dt = t[1] - t[0]
        yf = 2.0 / N * np.abs(fft(y)[0:N // 2])
        xf = np.fft.fftfreq(N, d=dt)[0:N // 2]
        return xf, yf

    def SaveToCSV(self, y, name):
        xf, yf = self.TransformataFouriera(y)
        data = {"xf": xf, "yf": yf}
        dataframe = pd.DataFrame(data, columns=("xf", "yf"))
        dataframe.to_csv("%s.csv" % name, index=False, sep=",", columns=["xf", "yf"], header=["xf", "yf"])
        print("Zapisano dane")

    def SaveToWav(self, y, name):
        audio_data = np.int16(y * 2**15)
        write('%s.wav'%name, self.sampling, audio_data)

