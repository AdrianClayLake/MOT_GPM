#!/usr/bin/env python
#title           :MOT_fpga_class_adc.py
#description     :Fits voltage curve data from magneto optical trap
#author          :
#email           :
#date            :09.01.2018
#version         :2
#notes           :
#python_version  :3.6 (Tested)
#==============================================================================
"""
Fits voltage curve data from magneto optical trap
@author: Adrian Lake
"""
from __future__ import print_function
import pickle as pk
import numpy as np
import matplotlib.pyplot as pl
import os, sys
from scipy.optimize import curve_fit
from time import time

# TODO,
# findout why the exponential curve has the last blakc on the bit
# do error analysis
# determin whether I should fit after or before scaling data from std

# sample last section of data
#ignore the last part of the test img
#fit the last bit of the loading rate with a linear graph


# what should we fit to the linear img settings

stdFunc = lambda x, a: x*0 + a # fit function
stdCrop = (0, -1) # interval to crop data
stdDefa = 5.0 # guss for fit
def stdFit(xData, yData):
    a, cov = curve_fit( stdFunc,
                                xData[stdCrop[0]:stdCrop[1]],
                                yData[stdCrop[0]:stdCrop[1]],
                                p0 = stdDefa)
    return  a[0], cov

imgFunc = lambda x, a, b: a*x + b # fit function
imgCrop = (0, -1) # interval to crop data
imgDefa = 0.1, 5.0 # guss for fit
def imgFit(xData, yData):
    (a, b), cov = curve_fit( imgFunc,
                                xData[stdCrop[0]:stdCrop[1]],
                                yData[stdCrop[0]:stdCrop[1]],
                                p0 = imgDefa)
    return  a, b, cov


#expFunc = lambda x, a, b, c: a*(1 - np.exp(-b*x)) + c # fit function
expFunc = lambda x, a, b, c: a*(1 - np.exp(-b*x))/b + c # fit function
linFunc = lambda x, a, c: a*x + c
expCrop = (0, -1) # interval to crop data
expDefa = 1.0, 1./20., 0.5 # guess for fit
def expFit(xData, yData, y0 = None):
    
#    if (yData[expCrop[1]]-yData[expCrop[0]]) < 0.05: # catch a null MOT
#            raise Exception('No fit possible, null MOT')

    (a, c), cov = curve_fit( linFunc,
                                    xData[expCrop[0]:expCrop[1]],
                                    yData[expCrop[0]:expCrop[1]],
                                    p0 = (expDefa[0], yData[expCrop[0]]))

    (a, b, c), cov = curve_fit( lambda x, a, b, c: expFunc(x, a, b, c if y0 is None else y0),
                                xData[expCrop[0]:expCrop[1]] - xData[expCrop[0]],
                                yData[expCrop[0]:expCrop[1]],
                                p0 = (a, expDefa[1], yData[expCrop[0]]),
                                bounds = ([0.0, 0.01, -np.inf ],
                                          [np.inf, np.inf, np.inf ]))

#    if (yData[expCrop[1]]-yData[expCrop[0]]) < 0.05: # catch a null MOT
#    if b < 0.0001: # catch a null MOT
#            raise Exception('No fit possible, null MOT')

    return  a, b, c, cov


def fitSample(data, verbose = 1):
    
    pl.figure()
    pl.cla()
    pl.clf()
    
    intervals = {'stdInt': (np.argwhere(data[:, 0] == 6)[0][0],
                            np.argwhere(data[:, 0] == 10.5)[0][0],),
                 'expInt': (np.argwhere(data[:, 0] == 10.5)[0][0],
                            np.argwhere(data[:, 0] == 40)[0][0],),
                 'imgInt': (np.argwhere(data[:, 0] == 41)[0][0],
                            np.argwhere(data[:, 0] == 45)[0][0],),
                 'finInt': (np.argwhere(data[:, 0] == 46)[0][0],
                            np.argwhere(data[:, 0] == 50)[0][0],)}


    if verbose:
        pl.plot(data[:, 0], data[:, 1], 'b')
        # interval plotting
        for i in intervals:
            print(i)
            a, b = intervals[i]
            pl.axvline(x=data[a, 0], color='r')
            pl.axvline(x=data[b, 0], color='r')
            pl.plot(data[a:b, 0], data[a:b, 1], 'g')
            # carefull, the fit may be cropped in above func



    ## FIT INDIVIDUAL REGIONS

    # std portion
    a, b = intervals['stdInt']
    stdRes = res = stdFit(data[a:b, 0], data[a:b, 1])
    if verbose:
        print('Fit Results: a \n a = {:}\n cov:\n{:}'.format(*res))
        pl.plot(data[a:b, 0], stdFunc(data[a:b, 0], res[0]), 'r')

    # standard portion
    a, b = intervals['expInt']
    expRes = res = expFit(data[a:b, 0], data[a:b, 1], y0 = stdRes[0])
    if verbose:
        if expRes[1] is None:
            print('Fit Results: a*x + c \n a = {:}\n b = {:}\n c = {:}\n cov:\n{:}'.format(*res))
            pl.plot(data[a:b, 0], linFunc(data[a:b, 0], res[0], res[2]), 'r')
        else:
            print('Fit Results: a*(1 - np.exp(-b*x)) + c \n a = {:}\n b = {:}\n c = {:}\n cov:\n{:}'.format(*res))
            pl.plot(data[a:b, 0], expFunc(data[a:b, 0] - data[a, 0], res[0], res[1], res[2]), 'r')


    a, b = intervals['imgInt']
    imgRes = res = imgFit(data[a:b, 0], data[a:b, 1])
    if verbose:
        print('Fit Results: ax + b \n a = {:}\n b = {:}\n cov:\n{:}'.format(*res))
        pl.plot(data[a:b, 0], imgFunc(data[a:b, 0], res[0], res[1]), 'r')

    a, b = intervals['finInt']
    finRes = res = stdFit(data[a:b, 0], data[a:b, 1])
    if verbose:
        print('Fit Results: a \n a = {:}\n cov:\n{:}'.format(*res))
        pl.plot(data[a:b, 0], stdFunc(data[a:b, 0], res[0]), 'r')




    a = imgRes[0]*data[intervals['imgInt'][0], 0] + imgRes[1] #img setting
    b = finRes[0] # img baseline
    c = expRes[0]/expRes[1] + expRes[2] # test load
    d = stdRes[0] # test baseline


    error = None #TODO: error analysis
    
    output = (expRes[0]*((a - b)/(c - d)), 
            (c - d)/(a - b), 
            expRes[1]), (error,)


    # formatting for plot calls above
    pl.title('ADC Voltage Curve'); pl.xlabel('t'); pl.ylabel('V(t)');
    pl.text(15,0.4, '$R_V$: {:1.3f}'.format(output[0][0]), fontsize=15)
    pl.text(15,0.35, '$f_ex$: {:1.3f}'.format(output[0][1]), fontsize=15)
    pl.text(15,0.3, '$\Gamma$: {:1.3f}'.format(output[0][2]), fontsize=15)

#    pl.savefig('Plot.png', dpi=800)
    pl.show()

    return output

if __name__ == '__main__':
    from MOTControl import sampleMOT
    # (b, pi, pt, ri, rt):
    x, y, settings = sampleMOT(0.5, 0.4, 85, 0.15 , 90)
    data = np.array([x, y]).T
    fitSample(data)
