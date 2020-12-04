from scipy import signal
import numpy as np

x= np.array([1,2,3,4,5,6,7,8,9,10])
q=3
d=signal.decimate(x, q, n=None, ftype='iir', axis=-1)

print ("x", len(x))
print ("d",len(d))
