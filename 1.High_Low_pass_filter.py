import h5py
import matplotlib.pyplot as plt
import time
import pandas as pd
from scipy import signal
import scipy.fftpack
import numpy as np
import pyts
from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt

#1. Dataset
#1.1 Read data
f=h5py.File("experiment_1.nwb","r")
x_eeg = f["acquisition/timeseries/recording1/continuous/processor105_100/data"]
y_eeg_int = list(range(0, len(x_eeg[0])))
y_eeg=map(str, y_eeg_int)
df=pd.DataFrame(x_eeg, columns=y_eeg)
data_1_piezo_row = df["132"]
data_2_ther_row = df["135"]

#1.2 Band-pass filter
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y

def butter_highpass(cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y


fps=2000     
lowcut = 3
highcut = 2

data_1_piezo_filt_numpy_high = butter_highpass_filter(data_1_piezo_row,highcut, fps)
data_2_ther_filt_numpy_high = butter_highpass_filter(data_2_ther_row,highcut, fps)

data_1_piezo_filt_numpy = butter_lowpass_filter(data_1_piezo_filt_numpy_high, lowcut, fps)
data_1_piezo_filt = pd.DataFrame(data_1_piezo_filt_numpy)
data_2_ther_filt_numpy = butter_lowpass_filter(data_2_ther_filt_numpy_high, lowcut, fps)
data_2_ther_filt = pd.DataFrame(data_2_ther_filt_numpy)



# 1.3. Denoisnig  
# Create synthetic signal
def Denoisnig(data):
    dt = 1
    data_denois=data
    t = np.arange(0, len(data_denois), 1)
    #signal = np.sin(2*np.pi*50*t) + np.sin(2*np.pi*120*t) #composite signal
    signal = data_denois
    signal_clean = signal #copy for later comparison
    signal = signal + 2.5 * np.random.randn(len(t))
    minsignal, maxsignal = signal.min(), signal.max()
    ## Compute Fourier Transform
    n = len(t)
    fhat = np.fft.fft(signal, n) #computes the fft
    psd = fhat * np.conj(fhat)/n
    freq = (1/(dt*n)) * np.arange(n) #frequency array
    print ("freq", freq)
    idxs_half = np.arange(1, np.floor(n/2), dtype=np.int32) #first half index
    ## Filter out noise
    threshold = 100
    psd_idxs = psd > threshold #array of 0 and 1
    psd_clean = psd * psd_idxs #zero out all the unnecessary powers
    fhat_clean = psd_idxs * fhat #used to retrieve the signal
    signal_denois = np.fft.ifft(fhat_clean) #inverse fourier transform
    signal_denois=pd.DataFrame(signal_denois)
    return signal_denois

#2.Graph
#figure, (ax1) = plt.subplots(1, 1, sharex=True)
#plt.plot(data_2_ther_filt)
#plt.show()
steps = 100
ofsett_graph=1000


data_for_graph_1=data_1_piezo_filt_numpy
data_for_graph_2=data_2_ther_filt_numpy


for number in range (0, x_eeg.shape[0], steps):
    #break
    plt.cla()
    plt.plot(data_for_graph_1[number:number+ofsett_graph])  #
    plt.plot(data_for_graph_2[number:number+ofsett_graph])   # ,color = '#0a0b0c'
    plt.xlabel('Ось X')
    plt.ylabel('Ось Y')
    plt.title('Black - Thermocouple, Blue - Piezo signal')
    plt.pause(0.000001)
    plt.draw()
    time.sleep(0.3)

#3.Correlation
#3.1.Spicy - Pearson
def correlation():    
    from scipy.stats import pearsonr    
    corr, _=pearsonr(data_1_piezo_filt_numpy, data_2_ther_filt_numpy)   #Pearson’s correlation coefficient, 2-tailed p-value
    print('Pearsons correlation',corr)
#3.2.Numpy Cov
    from numpy import cov
    covariance = cov(data_1_piezo_filt_numpy, data_2_ther_filt_numpy) #Covariance matrix
    print("Covariance matrix", covariance)
#3.3.Spearman’s Correlation 
    from scipy.stats import spearmanr
    corr, _ = spearmanr(data_1_piezo_filt_numpy, data_2_ther_filt_numpy)
    print("Spearman’s Correlation",corr)
    return True
#correlation()

#4.Fast_furier
def Fast_furier(data1, data2):
    figure, axis = plt.subplots(1, 1)
    plt.subplots_adjust(hspace=1)
    axis.set_title('Fourier transform depicting the frequency components')
    axis.set_xlabel('Frequency')
    axis.set_ylabel('Amplitude')
    for data in (data1, data2):
        fourierTransform = np.fft.fft(data)/len(data)           
        fourierTransform = fourierTransform[range(int(len(data)/2))] 
        tpCount     = len(data)
        values      = np.arange(int(tpCount/2))
        timePeriod  = tpCount/fps
        frequencies = values/timePeriod
        axis.plot(frequencies, abs(fourierTransform))        

    axis.axis([0, 20, 0, 5])          
    plt.show()

Fast_furier(data_for_graph_1, data_for_graph_2)

#5.spectral-temporal analysis python
def spectral(data):
    #f, t, Sxx = signal.spectrogram(data, 2000)
    #plt.figure(figsize=(8,10))
    #plt.pcolormesh(t, f, Sxx, shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.specgram(data,Fs=2000)
    plt.show()
#spectral (data_1_piezo_row)


#6. Coherence

def Coherence(data1,data2):
    plt.subplots_adjust(wspace=0.5)
    dt = 0.01
    t = np.arange(0, len(data_1_piezo_row), 1)
    s1 =  data1#0.01*np.sin(2*np.pi*10*t) + cnse1
    s2 =  data2 #0.01*np.sin(2*np.pi*10*t) + cnse2

    plt.subplot(211)
    plt.plot(t, s1, t, s2)
    plt.xlim(0, len(data_1_piezo_row))
    plt.xlabel('time')
    plt.ylabel('s1 and s2')
    plt.grid(True)

    plt.subplot(212)
    cxy, f = plt.cohere(s1, s2, 256, 1./dt)
    plt.ylabel('coherence')
    plt.show()

#Coherence(data_1_piezo_row,data_2_ther_row)

# 6.1 spectral power for signnals
def spectral_power(s1,s2):
    dt = 0.01
    plt.subplot(121)
    plt.psd(s1, 256, 1/dt)
    plt.title('signal1')

    plt.subplot(122)
    plt.psd(s2, 256, 1/dt)
    plt.title('signal2')

    plt.tight_layout()
    plt.show()
spectral_power(data_1_piezo_row,data_2_ther_row)

#6.2 coherent
def coherent (s1,s2):
    csdxy, fcsd = plt.csd(s1, s2, 256, 1./dt)
    plt.ylabel('CSD (db)')
    plt.title('cross spectral density between signal 1 and 2')
    plt.tight_layout()
    plt.show()
#coherent(data_1_piezo_row,data_2_ther_row)

#6.2
# coherence
from matplotlib import mlab
s1=data_1_piezo_filt_numpy
s2=data_2_ther_filt_numpy
dt = 0.1
# First create power sectral densities for normalization
(ps1, f) = mlab.psd(s1, Fs=1./dt, scale_by_freq=False)
(ps2, f) = mlab.psd(s2, Fs=1./dt, scale_by_freq=False)
plt.plot(f, ps1)
plt.plot(f, ps2)

# Then calculate cross spectral density
(csd, f) = mlab.csd(s1, s2, NFFT=256, Fs=1./dt,sides='default', scale_by_freq=False)
fig = plt.figure()
ax1 = fig.add_subplot(1, 2, 1)
# Normalize cross spectral absolute values by auto power spectral density
ax1.plot(f, np.absolute(csd)**2 / (ps1 * ps2))
ax2 = fig.add_subplot(1, 2, 2)
angle = np.angle(csd, deg=True)
angle[angle<-90] += 360
ax2.plot(f, angle)

# zoom in on frequency with maximum coherence
ax1.set_xlim(9, 11)
ax1.set_ylim(0, 1e-0)
ax1.set_title("Cross spectral density: Coherence")
ax2.set_xlim(9, 11)
ax2.set_ylim(0, 90)
ax2.set_title("Cross spectral density: Phase angle")

plt.show()
fig = plt.figure()
ax = plt.subplot(111)

ax.plot(f, np.real(csd), label='real')
ax.plot(f, np.imag(csd), label='imag')

ax.legend()
plt.show()
