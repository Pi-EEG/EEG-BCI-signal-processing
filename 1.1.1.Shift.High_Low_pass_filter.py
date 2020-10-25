import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import serial
import time
ComPort = serial.Serial('COM8') 
ComPort.baudrate = 115200          
ComPort.bytesize = 8            
ComPort.parity   = 'N'           
ComPort.stopbits = 1
random_data = np.arange(50)
name_of_dataset = np.arange(2)

def receive_data():
 for i in range(0,50,1):
  random_data[i] = int(ComPort.readline())
 return random_data

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


sines=receive_data()
sine = pd.DataFrame({'data0': sines} )
sine ['data1'] = sine

while 1:
 for a in range (0,2,1):    
  sines=receive_data() 
  sines1 = pd.DataFrame({'data'+str(a): sines} )
  sine ['data'+str(a)] = sines1

# ok 
  if a==0:
   zarem =  sine ['data'+str(a)].append(sine ['data'+str(a+1)])
   print (zarem)
  else:
   zarem =  sine ['data'+str(a)].append(sine ['data'+str(a-1)])
  
# stop  
  filtered_sine  =  butter_lowpass_filter(zarem.data, cutoffs, fps) 
# ax1.plot(range(axis_x, axis_x+50,1),sine,color = '#0a0b0c') 
  ax2.plot(range(axis_x, axis_x+51,1),filtered_sine[49:], color = '#0a0b0c')
  axis_x1_move = 1000 #sine["data"]
# ax1.axis([axis_x-400, axis_x+200, axis_x1_move[48]-200000, axis_x1_move[48]+200000])
  ax2.axis([axis_x-200, axis_x+200, filtered_sine[48]-5000, filtered_sine[48]+5000]) 
  axis_x=axis_x+50
  plt.pause(0.001)
  plt.draw()
#  plt.show()
