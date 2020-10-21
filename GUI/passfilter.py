import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import serial
import time


def butter_highpass(cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    print ("high filter")
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    print ("high filter")
    return y

def butter_lowpass(cutoff, fs, order=5):   
    nyq = 0.5 * fs
    print ("lowpass filter2") 
    normal_cutoff = cutoff / nyq
    print ("lowpass filter3") 
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    print ("lowpass filter4")
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    print ("lowpass filter")
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    
    return y





          

 
 


 


