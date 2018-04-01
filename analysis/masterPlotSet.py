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
clean = np.argwhere(data[7,:] < 10.).T[0]
data = data[:,clean]


bField = data[0,:]
pumpIntensity = data[1,:]
pumpAOMFreq = data[2,:]
repumpIntensity = data[3,:]
repumpAOMFreq = data[4,:]
depthR_v = data[5,:]
f_ex = data[6,:]


                     
#dataTablePath = './fitData_varried_image.csv' # path to for data fitting
#dataVI = np.genfromtxt(dataTablePath, delimiter = ',', comments='#').T
#clean = np.argwhere(data[7,:] < 200).T[0]
#data = data[:,clean]


#mInexes = np.array([0, 2, 4]) # matchedInedexs
#matches = np.array([m 
#                    for m, pVI in enumerate(dataVI.T)
#                    for n, p in enumerate(data.T) 
#                    if np.array_equal(p[mInexes], pVI[mInexes])])                    

#f_exVI = dataVI[6,:][matches]
#x = dataVI[6,:][matches]
#y = depthR_v[:y.shape[0]]

tuning = lambda f: 2*f - 180


def union(a1, a2):
    return

def steps(array):
    return np.array([np.argwhere(array == val)[:,0] for val in set(array)])

markers = "o^sdv"*5
#colors = np.repeat([0.0, 0.2, 0.4, 0.6], 5)
colors = np.tile([0.0, 0.2, 0.4, 0.6], 5)
colors = "cgbk"
polyFitDeg = 3
kernel = RBF()
def levelPlot(a, b, c, d, dVal, skip = 1):
    global xs, ys, model
    cSteps = steps(c)
    dLevel = np.argwhere(d == dVal)[:,0]
    xs = []; ys = [] # lists for fitting
    model = GaussianProcessRegressor(kernel=kernel, alpha=0.05)
    for s, cl, m in zip(cSteps[:], colors, markers):
        step = np.intersect1d(s, dLevel)
        sort = np.argsort(a[step])
        pl.plot(a[step][sort], b[step][sort], color = str(cl), marker = m, linewidth=0, label=str(c[s[0]]))        
#        fitable = np.argwhere(b[step][sort] < 10.0) # drop points that are oviously caused by an error, talk to madison
        xs += list(a[step][sort])
        ys += list(b[step][sort])
    ys = np.array(ys)
    xs = np.array(xs)
#    model.fit(xs.reshape(-1, 1), ys.reshape(-1, 1))
    x = np.linspace(*pl.xlim(), 1000)
#    pl.plot(x, model.predict(x.reshape(-1, 1)), 'k--')
    



levelPlot(tuning(pumpAOMFreq), depthR_v, repumpAOMFreq, bField, 0.8)
pl.xlabel("Pump Detuning"); pl.ylabel('$R_V$');
pl.grid(True)
pl.ylim(0.03, 0.06)
pl.legend(loc=(1.04,0.55))
fname = 'pumpVsRv'
pl.savefig(fname+'.eps', bbox_inches = 'tight', dpi=1000)
pl.show()


levelPlot(tuning(repumpAOMFreq), depthR_v, pumpAOMFreq, bField, 0.8)
pl.xlabel("Repump Detuning"); pl.ylabel('$R_V$');
pl.grid(True)
#pl.ylim(0.03, 0.06)
pl.legend(loc=(1.04,0.55))
fname = 'repumpVsRv'
pl.savefig(fname+'.eps', bbox_inches = 'tight', dpi=1000)
pl.show()


levelPlot(tuning(pumpAOMFreq), f_ex, repumpAOMFreq, bField, 0.6)
pl.xlabel("Pump Detuning"); pl.ylabel(r"$f_e^L/f_e^I$");
pl.grid(True)
#pl.ylim(0.0, 0.5)
pl.legend(loc=(1.04,0.55))
fname = 'pumpVsfexc'
pl.savefig(fname+'.eps', bbox_inches = 'tight', dpi=1000)

pl.show()


levelPlot(tuning(repumpAOMFreq), f_ex, pumpAOMFreq, bField, 0.8)
pl.xlabel("Repump Detuning"); pl.ylabel(r"$f_e^L/f_e^I$");
pl.grid(True)
#pl.ylim(0.0, 0.5)
pl.legend(loc=(1.04,0.55))
fname = 'repumpVsfexc'
pl.savefig(fname+'.eps', bbox_inches = 'tight', dpi=1000)
pl.show()


#levelPlot(pumpIntensity, depthR_v, pumpAOMFreq, bField, 0.8)
#pl.xlabel("Repump Detuning"); pl.ylabel('$R_V$');
#pl.grid(True)
#pl.ylim(0.0, 0.5)
#pl.savefig('destination_path.eps', dpi=1000)
#pl.show()
#
#levelPlot(repumpIntensity, depthR_v, pumpAOMFreq, bField, 0.8)
#pl.xlabel("Repump Detuning"); pl.ylabel('$R_V$');
#pl.grid(True)
#pl.ylim(0.0, 0.5)
#pl.savefig('destination_path.eps', dpi=1000)
#pl.show()




#pl.plot(depthR_v, f_ex, '.')
#pl.xlabel(r"$f_e^L/f_e^I$"); pl.ylabel('$R_V$');
#pl.grid(True)
#pl.savefig('destination_path.eps', dpi=1000)
#pl.xlim(0.0, 1.0)
#pl.ylim(0.0, 5.0)
#pl.show()


levelPlot(f_ex, depthR_v, pumpAOMFreq, bField, 0.8)
pl.xlabel(r"$f_e^L/f_e^I$"); pl.ylabel('$R_V$');
pl.grid(True)
pl.legend(loc=(1.04,0.55))
fname = 'fexcVsRv'
pl.savefig(fname+'.eps', bbox_inches = 'tight', dpi=1000)
pl.savefig(fname+'.png', bbox_inches = 'tight')
pl.show()


