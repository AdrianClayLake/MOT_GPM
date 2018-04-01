# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 11:08:51 2018

@author: Adrian
"""

import numpy as np
import matplotlib.pyplot as pl
from scipy.optimize import curve_fit

defualts = (1.0, 10., 0.1, 0.15, 40.0, 0.1, 1.65, 45.0, 0.8)

def curveFunc(x, c1, t1, r, g, t2, m, c2, t3, c3):

    if   x < t1:
        return c1
    elif x < t2:
        return r*(1-np.exp(-g*(x-t1)))/g + c1
        
    elif x < t3:
        return m*(x - t2) + c2
    else:
        return c3

curveFunc = np.vectorize(curveFunc)


def fitSample(data, verbose = 1):
    
    pl.figure()
    pl.cla()
    pl.clf()
    
    # fitting window
    a = np.argwhere(data[:, 0] == 5.0)
    b = np.argwhere(data[:, 0] == 50.0)
    fit, cov = curve_fit(data[a:b, 0], data[a:b, 1], curveFunc, po = defualts)
    c1, t1, r, g, t2, m, c2, t3, c3 = fit

    a = imgRes[0]*data[intervals['imgInt'][0], 0] + imgRes[1] #standard setting
    b = finRes[0] # standard baseline
    c = expRes[0]/expRes[1] + expRes[2] # test load
    d = stdRes[0] # test baseline


    error = None #TODO: error analysis
    
    output = (expRes[0]*((a - b)/(c - d)), 
            (c - d)/(a - b), 
            expRes[1]), (error,)


    # formatting for plot calls above
    pl.title('ADC Voltage Curve'); pl.xlabel('t'); pl.ylabel('V(t)');
    pl.text(15,0.6, '$R_V$: {:1.3f}'.format(output[0][0]), fontsize=15)
    pl.text(15,0.5, '$f_ex$: {:1.3f}'.format(output[0][1]), fontsize=15)
    pl.text(15,0.4, '$\Gamma$: {:1.3f}'.format(output[0][2]), fontsize=15)


    pl.show()


    pl.title('Normalized Voltage Curve'); pl.xlabel('t'); pl.ylabel('V(t)')
    pl.plot(data[:, 0], yNorm)
        

    pl.show()

    return output

if __name__ == '__main__':
    x = np.linspace(5, 50, 1000)
    
    pl.plot(x, curveFunc(x, *defualts))