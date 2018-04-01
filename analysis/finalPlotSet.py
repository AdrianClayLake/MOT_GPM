# -*- coding: utf-8 -*-
#!/usr/bin/env python
#title           :masterPlotSet.py
#description     : Produce all plots for a perticular dataset
#author          :
#email           :
#date            :09.01.2018
#version         :2
#notes           :
#python_version  :3.6
#==============================================================================
from __future__ import print_function

if __name__ == '__main__':
    import os
    os.chdir('../')

import numpy as np
import matplotlib.pyplot as pl
pl.style.use(r"prl.mplstyle")

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

dataTablePath = './fitData.csv' # path to for data fitting
data = np.genfromtxt(dataTablePath, delimiter = ',', comments='#').T


bField = data[0,:]
pumpIntensity = data[1,:]
pumpAOMFreq = data[2,:]
repumpIntensity = data[3,:]
repumpAOMFreq = data[4,:]
depthR_v = data[5,:]
f_ex = data[6,:]
gamma = data[7,:]

dev = 0.0006
mean = np.mean(depthR_v)
selection = np.argwhere(np.logical_and(depthR_v < mean + dev, depthR_v > mean - dev ))

##pl.title("Loss Rate Vs. Excited State Fraction")
#pl.xlabel("$f_{exc}$"); pl.ylabel('$\Gamma$');
#pl.plot(f_ex[selection], gamma[selection], '+')
#pl.plot(f_ex, gamma, '+')
#pl.savefig('gamma vs. f_exc.png', bbox_inches = 'tight', dpi=1000)
#pl.show()
#
#
#pl.hist(depthR_v)
##pl.hist(depthR_v[selection])
##pl.title('Iso-level $\hat{R}_v$ Histogram')
#pl.ylabel("$counts$"); pl.xlabel('$\hat{R}_v$');
#pl.savefig('Rv hist .png', bbox_inches = 'tight', dpi=1000)
#
#pl.show()



##pl.title("Loss Rate Vs. Excited State Fraction")
#pl.xlabel("$f_{exc}$"); pl.ylabel('$depthR_v$');
##pl.plot(f_ex[selection], depthR_v[selection], '+')
#pl.plot(f_ex, depthR_v, '+')
#pl.savefig('gamma vs. f_exc.png', bbox_inches = 'tight', dpi=1000)
#pl.show()



#pl.title("Loss Rate Vs. Excited State Fraction")
#pl.xlabel("$f_{exc}$"); pl.ylabel('$pumpAOMFreq$');
#pl.plot(f_ex[selection], depthR_v[selection], '+')
pl.plot(pumpAOMFreq, pumpIntensity, '+')
pl.savefig('gamma vs. f_exc.png', bbox_inches = 'tight', dpi=1000)
pl.show()

pl.plot((pumpAOMFreq - 80)/10, '+')
pl.plot(pumpIntensity, '^')
pl.plot(depthR_v*100, '.')
pl.show()


