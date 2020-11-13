import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import serial
import time
import matplotlib.pyplot as plotter

ComPort = serial.Serial('COM7') 
ComPort.baudrate = 115200          
ComPort.bytesize = 8            
ComPort.parity   = 'N'           
ComPort.stopbits = 1
random_data = np.arange(500)
def receive_data():
 t0 = time.perf_counter() 
 for i in range(0,500,1):
  random_data[i] = int(ComPort.readline())
 result = pd.DataFrame({'data': random_data} )
 t1 = time.perf_counter() - t0
 global fs
 fs = int (500/t1)
 return result

def butter_highpass(cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

def butter_lowpass(cutoffs, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoffs, fs, order=5):
    b, a = butter_lowpass(cutoffs, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y

#order = 6
fps=fs = 10     # sample rate, Hz
cutoffs = 30
cutoff=2

figure, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
axis_x=0
while 1:
 sine = receive_data()
 print ("sine",sine)
 
 fourierTransform = np.fft.fft(sine.data)/len(sine.data)           #
 fourierTransform = fourierTransform[range(int(len(sine.data)))]
 fourier = fourierTransform[range(int(len(sine.data)/2))]
 print ("fourierTransform",len (fourierTransform))

 tpCount     = len(sine.data)
 values      = np.arange(int(tpCount/2))
 timePeriod  = tpCount/fs
 frequencies = values/timePeriod


 ax1.plot(range(axis_x, axis_x+500,1),sine,color = '#0a0b0c') 
 ax2.plot(range(axis_x, axis_x+500,1),abs (fourierTransform), color = '#0a0b0c')
 axis_x1_move=sine["data"]
 ax1.axis([axis_x-4000, axis_x+2000, axis_x1_move[48]-200000, axis_x1_move[48]+200000])
 ax2.axis([-4000, +2000,-5000, +5000]) 
 axis_x=axis_x+500

 figure, axis = plotter.subplots(1, 1)
 axis.set_title('Fourier transform depicting the frequency components')
 axis.plot(frequencies, (abs(fourier)))
 axis.set_xlabel('Frequency')
 axis.set_ylabel('Amplitude')

 
 plt.pause(0.001)
 plt.draw()
 break
#plt.show()
