'''
Shows simple sound processor with fft

Inspired by `Basic Sound Processing with Python <http://samcarcagno.altervista.org/blog/basic-sound-processor-python/>`_
'''
import sys, os

from pylab import fft, arange, log10, ceil
from scipy.io import wavfile
from matplotlib.pyplot import ylabel, xlabel, subplots, show

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from util.fft_util import FFTUtil
import numpy as np


def getFFT(s1, n):
    p = fft(s1) # take the fourier transform
    nUniquePts = ceil((n + 1) / 2.0)
    p = p[0:nUniquePts]
    p = abs(p)
    p = p / n # scale by the number of points so that
    # the magnitude does not depend on the length
    # of the signal or on its sampling frequency
    p = p ** 2 # square it to get the power
# multiply by two (see technical document for details)
# odd nfft excludes Nyquist point
    if n % 2 > 0: # we've got odd number of points fft
        p[1:len(p)] = p[1:len(p)] * 2
    else:
        p[1:len(p) - 1] = p[1:len(p) - 1] * 2 # we've got even number of points fft
    return nUniquePts, p

def getFFTUtil(s1, n):
    nUniquePts = ceil((n + 1) / 2.0)
    
    return nUniquePts, FFTUtil().fft(s1)


def main():

    path = "../../example/"
    #samplingRate, s1 = wavfile.read(path + '440_sine.wav')
    samplingRate, s1 = wavfile.read(path + '12000hz.wav')
    
    if len(s1.shape) == 2:
        s1 = s1[:,0]
    
    if len(s1) > 8192:
        s1 = s1[:256]
    
    n = float(len(s1))
    
    print "DType %s" % s1.dtype
    print "Sound File Shape " + str(s1.shape)
    print "Sample Frequency / Entries: %.2f / %.2f" % (samplingRate, n)
    print "Duration %.2f ms" % ((n / samplingRate)*1000)
    
    s1 = s1 / (2.**15)
    # Plotting the Tone
    timeArray = arange(0, n, 1)
    timeArray = timeArray / samplingRate
    timeArray = timeArray * 1000  #scale to milliseconds
    
    _, (axTone, axFreq, axLogFreq) = subplots(3)
    axTone.plot(timeArray, s1, color='k')
    ylabel('Amplitude')
    xlabel('Time (ms)')
    
    
    #Plotting the Frequency Content
    nUniquePts, p = getFFT(s1, n)
    #nUniquePts, p = getFFTUtil(s1, n)
    
    freqArray = arange(0, nUniquePts, 1.0) * (samplingRate / n);
    
    print "FreqMax %fHz" % freqArray[np.argmax(p)]
    
    axFreq.plot(freqArray/1000, p, color='k')
    axLogFreq.plot(freqArray/1000, 10*log10(p), color='k')
    
    
    xlabel('Frequency (kHz)')
    ylabel('Power (dB)')
    show()
    
if __name__ == "__main__":
    main()
