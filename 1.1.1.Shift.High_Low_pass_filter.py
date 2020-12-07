import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import serial
import time
ComPort = serial.Serial('COM7') 
ComPort.baudrate = 115200          
ComPort.bytesize = 8            
ComPort.parity   = 'N'           
ComPort.stopbits = 1
sample_len=100
random_data = np.arange(sample_len)

def receive_datas():
 for i in range(0,sample_len,1):
  random_data[i] = int(ComPort.readline())
 return random_data

sines=receive_datas()
sine = pd.DataFrame({'data': sines} )
zet=sine.values
sine ['data0'] = sine
sine ['data1'] = zet
sine ['data2'] = zet
sine ['data3'] = zet
sine ['data4'] = zet
sine ['data5'] = zet
sine ['data6'] = zet
sine ['data7'] = zet

def receive_data(a):
 t0 = time.perf_counter()
 for i in range(0,sample_len,1):
  random_data[i] = int(ComPort.readline())
 sine ['data'+str(a)] = random_data 
 if a==0:        
  z = np.append(sine ['data'], (sine ['data1']))            
  z = np.append(z, (sine ['data2']))
  z = np.append(z, (sine ['data3']))
  z = np.append(z, (sine ['data4']))
  z = np.append(z, (sine ['data5']))
  z = np.append(z, (sine ['data6']))
  z = np.append(z, (sine ['data7']))
  z = np.append(z, (sine ['data0']))
 if a==1:
  z = np.append(sine ['data'], (sine ['data2']))            
  z = np.append(z, (sine ['data3']))
  z = np.append(z, (sine ['data4']))
  z = np.append(z, (sine ['data5']))
  z = np.append(z, (sine ['data6']))
  z = np.append(z, (sine ['data7']))
  z = np.append(z, (sine ['data0']))
  z = np.append(z, (sine ['data1']))                      
 if a==2:
  z = np.append(sine ['data'], (sine ['data3']))            
  z = np.append(z, (sine ['data4']))
  z = np.append(z, (sine ['data5']))
  z = np.append(z, (sine ['data6']))
  z = np.append(z, (sine ['data7']))
  z = np.append(z, (sine ['data0']))
  z = np.append(z, (sine ['data1']))
  z = np.append(z, (sine ['data2']))                        
 if a==3:
  z = np.append(sine ['data'], (sine ['data4']))            
  z = np.append(z, (sine ['data5']))
  z = np.append(z, (sine ['data6']))
  z = np.append(z, (sine ['data7']))
  z = np.append(z, (sine ['data0']))
  z = np.append(z, (sine ['data1']))
  z = np.append(z, (sine ['data2']))
  z = np.append(z, (sine ['data3']))            
 if a==4:
  z = np.append(sine ['data'], (sine ['data5']))            
  z = np.append(z, (sine ['data6']))
  z = np.append(z, (sine ['data7']))
  z = np.append(z, (sine ['data0']))
  z = np.append(z, (sine ['data1']))
  z = np.append(z, (sine ['data2']))
  z = np.append(z, (sine ['data3']))
  z = np.append(z, (sine ['data4']))            
 if a==5:
  z = np.append(sine ['data'], (sine ['data6']))            
  z = np.append(z, (sine ['data7']))
  z = np.append(z, (sine ['data0']))
  z = np.append(z, (sine ['data1']))
  z = np.append(z, (sine ['data2']))
  z = np.append(z, (sine ['data3']))
  z = np.append(z, (sine ['data4']))
  z = np.append(z, (sine ['data5']))            
 if a==6:
  z = np.append(sine ['data'], (sine ['data7']))            
  z = np.append(z, (sine ['data0']))
  z = np.append(z, (sine ['data1']))
  z = np.append(z, (sine ['data2']))
  z = np.append(z, (sine ['data3']))
  z = np.append(z, (sine ['data4']))
  z = np.append(z, (sine ['data5']))
  z = np.append(z, (sine ['data6']))          
 if a==7:
  z = np.append(sine ['data'], (sine ['data0']))            
  z = np.append(z, (sine ['data1']))
  z = np.append(z, (sine ['data2']))
  z = np.append(z, (sine ['data3']))
  z = np.append(z, (sine ['data4']))
  z = np.append(z, (sine ['data5']))
  z = np.append(z, (sine ['data6']))
  z = np.append(z, (sine ['data7']))   

 t1 = time.perf_counter() - t0
 t1=t1*8
 global fps
 fps = int (sample_len/t1)
 print ("fps", fps)

 result = pd.DataFrame({'data': z} )
# result = result[:sample_len]
 return result

def butter_bandpass(lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a
def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y

cutoffs = 2
cutoff = 1
figure, (ax) = plt.subplots(1, 1, sharex=True)
axis_x=0
a=0
while 1:
 dataset = receive_data(a)
 a=a+1
 if (a == 7):
  a=0
 #dataset = dataset[:sample_len]
 # print ("sine",sine)

 filtered_sine = butter_bandpass_filter(dataset.data, cutoff, cutoffs, fps)
 print ("filtered_sine", len(filtered_sine))
 filtered_sine = filtered_sine[(sample_len*8):]
 print ("filtered_sine", len(filtered_sine))
 ax.plot(range(axis_x, axis_x+sample_len,1),filtered_sine, color = '#0a0b0c')
 ax.axis([axis_x-499, axis_x+501, filtered_sine[sample_len-1]-500, filtered_sine[sample_len-1]+500]) 
 axis_x=axis_x+sample_len
 print ("ok") 
 plt.pause(0.000001)
 plt.draw()
