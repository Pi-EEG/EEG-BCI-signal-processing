import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize    

from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random


from PyQt5.Qt import *
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
               
        self.setMinimumSize(QSize(300, 200))    
        self.setWindowTitle("PyQt button example - pythonprogramminglanguage.com") 
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
        self.setWindowTitle("PyQt button example - pythonprogramminglanguage.com1") 
              
       # self.figure = plt.figure(num=None, figsize=(0.2, 0.2), dpi=80, facecolor='r', edgecolor='r')
        self.figure = plt.figure(figsize=(0.01,0.01),facecolor='g') 
        #self.figure.set_facecolor("blue")
        
        self.figure1 = plt.figure(figsize=(1, 1)) #, dpi=100
        

        
        self.canvas = FigureCanvas(self.figure)
        self.figure.subplots_adjust(0.2, 0.2, 0.3, 0.3) 
        self.canvas1 = FigureCanvas(self.figure1)
        self.figure1.subplots_adjust(0.2, 0.2, 0.3, 0.3) 
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar1 = NavigationToolbar(self.canvas1, self)
        
        pybutton = QPushButton('swcond_win', self)        
        pybutton.clicked.connect(self.clickMethod)
        pybutton.move(350, 10)
        pybutton.resize(100,32)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(100,100,0,11)
        layout.setGeometry(QRect(0, 0, 80, 68))         
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)    
        layout.addWidget(self.toolbar1)
        layout.addWidget(self.canvas1)
        

       # 
        self.le_num1 = QLineEdit()
        self.le_num1.setFixedSize(10, 20) 
        #self.le_num1.resize(135, 140)
        self.pb_num1 = QPushButton('...')
        self.pb_num1.setFixedSize(10, 20) 
        #self.pb_num1.resize(135, 140)        
        self.pb_num1.clicked.connect(self.show_dialog_num1)       

        #layout1 = QGridLayout()        
        layout.addWidget(QLabel('num1')) 
        layout.addWidget(self.le_num1)
        layout.addWidget(self.pb_num1)

        self.setLayout(layout)
        self.setLayout(layout)
        
        
    def clickMethod(self):
        print('Clicked Pyqt button')
        
        data = [random.random() for i in range(10)]
        data1 = [random.random() for i in range(10)]
        self.figure.clear()
        self.figure1.clear()
        
        ax = self.figure.add_subplot(111)
        ax1 = self.figure1.add_subplot(111)
        
        ax.plot(data, '*-')
        ax1.plot(data1, '*-')
        self.canvas.draw()
        self.canvas1.draw()
        
# input data

    def show_dialog_num1(self):
        value, ok = QInputDialog.getInt(self, 'Input dialog', 'Enter your num1:')
        print (value)

       # mainWin.show()
       # seconWin.close()  

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    seconWin = second_window()
   
    
    sys.exit( app.exec_() )
