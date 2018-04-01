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
from sklearn.linear_model import LinearRegression

dataTablePath = './fitData.csv' # path to for data fitting
data = np.genfromtxt(dataTablePath, delimiter = ',', comments='#').T

                     
bField = data[0,:]
pumpIntensity = data[1,:]
pumpAOMFreq = data[2,:]
repumpIntensity = data[3,:]
repumpAOMFreq = data[4,:]
#depthR_v = data[5,:]
#depthr_v = data[5,:]
#depthGamma = data[5,:]

tuning = lambda f: 2*f-180


def union(a1, a2):
    return

def steps(array):
    return np.array([np.argwhere(array == val)[:,0] for val in set(array)])

markers = "o^sd"*5
#colors = np.repeat([0.0, 0.3, 0.6], 5)
colors = np.tile([0.0, 0.2, 0.4, 0.6], 5)
polyFitDeg = 3
def levelPlot(a, b, c, d, dVal, skip = 1):
    global xs, ys, model
    cSteps = steps(c)
    dLevel = np.argwhere(d == dVal)[:,0]
    xs = []; ys = [] # lists for fitting
    model = LinearRegression()
    for s, c, m in zip(cSteps[:], colors, markers):
        step = np.intersect1d(s, dLevel)
        sort = np.argsort(a[step])
        pl.plot(a[step][sort], b[step][sort], color = str(c), marker = m, linewidth=0) 
        fitable = np.argwhere(b[step][sort] < 10.0) # drop points that are oviously caused by an error, talk to madison
        xs += list(a[step][sort][fitable])
        ys += list(b[step][sort][fitable])
    ys = np.array(ys)
    xs = np.array(xs)
    model.fit(xs.reshape(-1, 1), ys.reshape(-1, 1))
    x = np.linspace(*pl.xlim(), 1000)
    
    pl.plot(x, model.predict(x.reshape(-1, 1)))
    



levelPlot(tuning(pumpAOMFreq), depthR_v, repumpAOMFreq, bField, 1.0)
pl.xlabel("Pump Detuning"); pl.ylabel('$R_V$');
pl.grid(True)
pl.ylim(0.0, 0.5)
pl.show()


levelPlot(tuning(repumpAOMFreq), depthR_v, pumpAOMFreq, bField, 0.8)
pl.xlabel("Repump Detuning"); pl.ylabel('$R_V$');
pl.grid(True)
pl.ylim(0.0, 0.5)
pl.show()


levelPlot(pumpIntensity, depthR_v, pumpAOMFreq, bField, 0.8)
pl.xlabel("Repump Detuning"); pl.ylabel('$R_V$');
pl.grid(True)
pl.ylim(0.0, 0.5)
pl.show()

levelPlot(repumpIntensity, depthR_v, pumpAOMFreq, bField, 0.8)
pl.xlabel("Repump Detuning"); pl.ylabel('$R_V$');
pl.grid(True)
pl.ylim(0.0, 0.5)
pl.show()
