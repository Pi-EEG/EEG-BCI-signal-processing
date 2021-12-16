import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import serial
import time
import threading
#from ringbuf import RingBuffer #to be implemented

#COM parameters
port='COM13'
baudrate = 115200          
bytesize = 8            
parity   = 'N'           
stopbits = 1

#display buffer
sample_len=150

#filter parameter init
highcut = 10
lowcut = 1
fs = 30 #to be determined (and fixed)
bandpass_a = 0
bandpass_b = 0

#plot init
plt.ion() 
figure, (ax) = plt.subplots(1, 1, sharex=True)
axis_x=0
a=0


def read_from_port():
	global  data_buffer, bufferComplete, mylogfile
	idx_buffer=0
	t = threading.currentThread()
	while getattr(t, "serialReading", True):
		curr_time = time.time()
		
		try:
			
			if not bufferComplete:
				if(idx_buffer < sample_len): 
					
					curr_data = int(ComPort.readline())
					data_buffer[idx_buffer] = curr_data
					idx_buffer += 1
					mylogfile.write(""+str(curr_time)+","+str(curr_data)+"\n")
				else:
					bufferComplete = True
					idx_buffer= 0
			
		except Exception as e: 
			print(e)

def butter_bandpass_coeff(lowcut, highcut, fs, order=5):
	global bandpass_b , bandpass_a
	nyq = 0.5 * fs
	low = lowcut / nyq
	high = highcut / nyq
	bandpass_b , bandpass_a = signal.butter(order, [low, high], btype='band')

def butter_bandpass_filter(data):
    return signal.filtfilt( bandpass_b , bandpass_a, data) #lfilter


if __name__ == '__main__':
	global  data_buffer,bufferComplete, mylogfile 
	
	data_buffer = np.arange(sample_len)
	bufferComplete = False
	
	#init serial communication
	ComPort = serial.Serial(port, baudrate, parity=parity, bytesize=bytesize, stopbits=stopbits, timeout=1)
	
	#init file log open
	mylogfile = open('loc_com_data.csv', "w")
	
	#init filter coefficents (must be called only if the cut frequencies change)
	butter_bandpass_coeff(lowcut, highcut, fs)
	
	t = threading.Thread(target=read_from_port)
	t.start()
	
	while True:
		if bufferComplete:
			tempBuff = data_buffer.copy() #safe copy to allow buffer to be filled again
			filtered_sine = butter_bandpass_filter(tempBuff)
			#print(tempBuff)

			ax.plot(range(axis_x, axis_x+sample_len,1),filtered_sine, color = '#0a0b0c')
			ax.axis([axis_x-499, axis_x+501, filtered_sine[sample_len-1]-2000, filtered_sine[sample_len-1]+2000]) 
			axis_x=axis_x+sample_len

			plt.pause(0.0001)
			plt.draw()

