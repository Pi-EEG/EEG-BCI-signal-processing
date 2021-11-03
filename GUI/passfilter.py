
  import numpy as np
 	import pandas as pd
 	from scipy import signal
 	import matplotlib.pyplot as plt
 	import serial
 	import time
 	 
 	# sosfiltfilt, sosfiltfilt, lfilter_zi, lfilter, lfiltic, savgol_filter, sosfilt
 	 
 	def butter_highpass(cutoff, fs, order=4):
 	 nyq = 0.5 * fs
 	 normal_cutoff = cutoff / nyq
 	 b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
 	 return b, a
 	 
 	def butter_highpass_filter(data, cutoff, fs, order=4):
  	b, a = butter_highpass(cutoff, fs, order=order)
  	y = signal.filtfilt(b, a, data)
  	return y
 	 
 	def butter_lowpass(cutoff, fs, order=4):
  	nyq = 0.5 * fs
  	normal_cutoff = cutoff / nyq
  	b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
  	return b, a
 	 
 	def butter_lowpass_filter(data, cutoff, fs, order=4):
  	b, a = butter_lowpass(cutoff, fs, order=order)
  	y = signal.lfilter(b, a, data)
  	return y
 	 
 	def butter_bandpass(lowcut, highcut, fs, order=5):
  	nyq = 0.5 * fs
  	low = lowcut / nyq
  	high = highcut / nyq
  	b, a = signal.butter(order, [low, high], btype='band')
  	return b, a
 	 
 	def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
  	b, a = butter_bandpass(lowcut, highcut, fs, order=order)
  	y = signal.lfilter(b, a, data)
  	return y
 	 
