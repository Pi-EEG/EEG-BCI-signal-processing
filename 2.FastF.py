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
 return result



#order = 6
fps=fs = 10     # sample rate, Hz
cutoffs = 30
cutoff=2

figure, (ax1) = plt.subplots(1, 1, sharex=True)
axis_x=0


figure, axis = plotter.subplots(1, 1)
axis.set_title('Fourier transform depicting the frequency components')
axis.set_xlabel('Frequency')
axis.set_ylabel('Amplitude') 

while 1:
 axis.clear()
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
# ax2.plot(range(axis_x, axis_x+500,1),abs (fourierTransform), color = '#0a0b0c')
 axis_x1_move=sine["data"]
 ax1.axis([axis_x-4000, axis_x+2000, axis_x1_move[48]-200000, axis_x1_move[48]+200000])
# ax2.axis([-4000, +2000,-5000, +5000]) 
 axis_x=axis_x+500

 

 axis.plot(frequencies, (abs(fourier)))

 plt.pause(0.001)
 plt.draw()

# break
#plt.show()
