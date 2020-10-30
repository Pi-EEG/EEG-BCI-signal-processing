import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize    
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5.Qt import *
import random
import threading 
import time
import numpy as np
import pandas as pd
from scipy import signal
import serial
import passfilter 

ComPort = serial.Serial('COM5') 
ComPort.baudrate = 115200          
ComPort.bytesize = 8            
ComPort.parity   = 'N'           
ComPort.stopbits = 1

global sample_len
sample_len=100

random_data = np.arange(sample_len)
def receive_data():
 for i in range(0,sample_len,1):
  random_data[i] = int(ComPort.readline())
 return random_data

sines=receive_data()
sine = pd.DataFrame({'data': sines} )
z=sine.values
sine ['data0'] = sine
sine ['data1'] = z
sine ['data2'] = z
sine ['data3'] = z
print (sine)
global cutoff
cutoff = 1
global cutoffs
cutoffs = 10


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
               
        self.setMinimumSize(QSize(300, 200))    
        self.setWindowTitle("BCI") 
        pybutton = QPushButton('Click me', self)        
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(100,32)
        pybutton.move(50, 50)        
    def clickMethod(self):
        print('Clicked Pyqt button.')

        seconWin.show()
        mainWin.close()

class second_window(QWidget):

    def __init__(self):
        print ("start")       
        QWidget.__init__(self)

        self.setMinimumSize(QSize(600, 500))    
        self.setWindowTitle("Iron_BCI") 
              
        self.figure = plt.figure(figsize=(0,2,),facecolor='y',  edgecolor='r') #  color only     
        self.figure1 = plt.figure(figsize=(0,2),facecolor='y') # color only
        self.figure2 = plt.figure(figsize=(0,2),facecolor='y')
        self.figure3 = plt.figure(figsize=(0,2),facecolor='y')
                
        self.canvas = FigureCanvas(self.figure)
        self.figure.subplots_adjust(0.2, 0.4, 0.8, 1)  # only graph 
        self.canvas1 = FigureCanvas(self.figure1)
        self.figure1.subplots_adjust(0.2, 0.4, 0.8, 1)  # only graph 
        self.canvas2 = FigureCanvas(self.figure2)
        self.figure2.subplots_adjust(0.2, 0.4, 0.8, 1)
        self.canvas3 = FigureCanvas(self.figure3)
        self.figure3.subplots_adjust(0.2, 0.4, 0.8, 1)
       # self.toolbar = NavigationToolbar(self.canvas, self)
       # self.toolbar1 = NavigationToolbar(self.canvas1, self)
        
        pybutton = QPushButton('graph', self)        
        global axis_x
        axis_x=0

        pybutton.clicked.connect(self.clickMethod)
        pybutton.move(450, 10)
        pybutton.resize(100,32)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(50,100,0,11) # move background
        layout.setGeometry(QRect(0, 0, 80, 68))# nothing  
      # layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)    
      # layout.addWidget(self.toolbar1)
        layout.addWidget(self.canvas1)        
        layout.addWidget(self.canvas2)  # background
        layout.addWidget(self.canvas3)
       # input dataufoff value  
        le_num1 = QLineEdit(self)
        le_num1.setFixedSize(60, 20) # size
        le_num1.move(230,10)  
        pb_num1 = QPushButton('HPS',self)
        pb_num1.setFixedSize(50, 60) # size
        pb_num1.clicked.connect(self.show_dialog_num1)
        #layout.addWidget(self.le_num1)       
        pb_num1.move(290, 10)        
       # layout.addWidget(self.pb_num1)
      #  self.setLayout(layout)
        # stop input data
        
        # start input data fps
        le_num2 = QLineEdit(self)
        le_num2.setFixedSize(50, 20) # size
        le_num2.move(120, 10) 
        pb_num2 = QPushButton('fs',self)
        pb_num2.setFixedSize(50, 60) # size
        pb_num2.clicked.connect(self.show_dialog_num2)       
        pb_num2.move(170, 10)        
        # stop input data fps
        
        # start input data low filter        
               
        pb_num3 = QPushButton('LPF',self)       
        pb_num3.setFixedSize(50, 60)
        pb_num3.move(60, 10)       
        pb_num3.clicked.connect(self.show_dialog_num3)
        le_num3=QLineEdit(str(cutoffs), self)
        le_num3.move(10, 10)                 
        le_num3.setFixedSize(50, 20)              
        #layout.addWidget(self.le_num3)       
        #layout.addWidget(pb_num3)
        self.setLayout(layout)
        # stop input data filter
    
    def clickMethod(self):

         for a in range (0,2,1):  
          try:
           t0 = time.perf_counter()            
           for i in range(0,sample_len,1):
            random_data[i] = int(ComPort.readline())
  
           t1 = time.perf_counter() - t0
           global fs
           fs = int (sample_len/t1)
          # sines1 = pd.DataFrame({'data'+str(a): random_data} )
           sine ['data'+str(a)] = random_data

           #sine ['data0'] = None
           #sine ['data1'] = None
           #sine ['data2'] = None
           #sine ['data3'] = None
           #sine ['data'] = None


           if a==0:
            z = np.append(sine ['data'], (sine ['data1']))            
            z = np.append(z, (sine ['data2']))
            z = np.append(z, (sine ['data3']))
            z = np.append(z, (sine ['data0']))
                               
            print ("z",len(z))
            
            ##zarem =  sine ['data'].append(sine ['data2'])
            #zarem =  sine ['data'].append(sine ['data3'])
            #zarem =  sine ['data'].append(sine ['data0'])
            
           if a==1:
            z = np.append(sine ['data'], (sine ['data2']))            
            z = np.append(z, (sine ['data3']))
            z = np.append(z, (sine ['data0']))
            z = np.append(z, (sine ['data1']))

           if a==2:

            z = np.append(sine ['data'], (sine ['data3']))            
            z = np.append(z, (sine ['data0']))
            z = np.append(z, (sine ['data1']))
            z = np.append(z, (sine ['data2']))
            
           if a==3:

            z = np.append(sine ['data'], (sine ['data0']))            
            z = np.append(z, (sine ['data1']))
            z = np.append(z, (sine ['data2']))
            z = np.append(z, (sine ['data3']))
            
            
          
           result_raw = pd.DataFrame({'data': z})
           print ("z", len(z))
          # print ("result_raw",result_raw)
 
           result_high  = passfilter.butter_highpass_filter(result_raw.data,cutoff, fs)
           result_low   = passfilter.butter_lowpass_filter(result_raw.data,cutoffs, fs)
           result_band  = passfilter.butter_bandpass_filter(result_raw.data, cutoff, cutoffs, fs)
         #print (result)
          except ValueError:
           print ("ValueError")
                                  
         data=result_raw
         bias_result_raw= int(data.sum()/sample_len)
         data=result_high
         bias_result_high= int(data.sum()/sample_len)
         data=result_low
         bias_result_low= int(data.sum()/sample_len)                 
         data=result_band
         bias_result_band= int(data.sum()/sample_len)
         ax =  self.figure.add_subplot(111)
         ax1 = self.figure1.add_subplot(111)
         ax2 = self.figure2.add_subplot(111)
         ax3 = self.figure3.add_subplot(111)
         #ax.plot(data, '*-')                         
         #ax.axis([0, 2000, 0, 20000])
         global axis_x
         #Raw_data
         #print ("result_raw",result_raw[:sample_len])
         ax.plot(range(axis_x, axis_x+sample_len,1),result_raw[-sample_len:],color = '#0a0b0c')
         ax.axis([axis_x-500, axis_x+500, bias_result_raw-2000, bias_result_raw+2000])  #
         #High-pass-filter       
         ax1.plot(range(axis_x, axis_x+sample_len,1),result_high[-sample_len:],color = 'b') 
         ax1.axis([axis_x-500, axis_x+500, bias_result_high-2000, bias_result_high+2000])  #
         #Low-pass-filter 
         ax2.plot(range(axis_x, axis_x+sample_len,1),result_low[-sample_len:],color = 'y') 
         ax2.axis([axis_x-500, axis_x+500, bias_result_low-2000, bias_result_low+2000])
         #Band_pass_filter
       #  print ("res1", len (result_band))
       #  result_band=result_band[50:]
       #  print ("re2",  len (result_band))
       #  result_band=result_band[:-50]
       #  print ("res",  len (result_band))
         
         ax3.plot(range(axis_x, axis_x+sample_len,1),result_band[-sample_len:],color = 'g') 
         ax3.axis([axis_x-500, axis_x+500, bias_result_band-2000, bias_result_band+2000]) 
         
         axis_x=axis_x+sample_len
         
         self.canvas.draw()
         self.canvas1.draw()
         self.canvas2.draw()
         self.canvas3.draw()
                 
         thread=threading.Thread(target=self.clickMethod, args=())
         thread.start()                
# input data
    def show_dialog_num1(self):
        value, r = QInputDialog.getInt(self, 'Input dialog', 'HPS:')
        global cutoff
        cutoff = value/10
        print (cutoff)
    def show_dialog_num2(self):
        value, r = QInputDialog.getInt(self, 'Input dialog', 'fs:')
        global fs
        fs = value
        print (fs)
    def show_dialog_num3(self):
        value, r = QInputDialog.getInt(self, 'Input dialog', 'LPF:')
        global cutoffs
        cutoffs = value
        print (cutoffs)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    seconWin = second_window()       
    sys.exit( app.exec_() )
