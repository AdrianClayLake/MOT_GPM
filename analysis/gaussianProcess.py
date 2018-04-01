#!/usr/bin/env python
#title           :MOT_fpga_class_adc.py
#description     :Samples MOT for TDS study
#author          :
#email           :
#date            :09.01.2018
#version         :2
#notes           :A patched version of the non ADC code to utilize the MC USB 16808 ADC
#python_version  :3.6 (Tested)
#==============================================================================
#doppler effectplaya major rol we cant hve trap at resonoca

if __name__ == '__main__':
    import os
    os.chdir('../')

from time import sleep, time
import numpy as np
import pickle as pk
from matplotlib import pyplot as pl
from matplotlib import cm
#from mpl_toolkits.mplot3d import Axes3D
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
import glob
from os.path import join
import analysis.depthFit as fit
import scipy.interpolate as interp

dataTablePath = './fitData.csv' # path to for data fitting
saveDir = './Output/' # path to for data fitting
saveKernel = False
saveModel = False
loadKernelPath = "" # does not load if path is invalid
updateInt = 1 # check for updates ever n seconds
matDisp = None
nPoints = 100 # number of  points per axis to sample the model at
interpolate = False # interpolate for easier reading, ONLY ENABLE WHEN KERNAL IS OPTIMIZED FOR EXP.
upScaleFactor = 3 # factor that nPoints is scaled by for inerpolation
expand = 0 # expansion factor for display
defaultArray = np.array([0.84, 0.35, 88.0, 0.22, 90.0]) # default array to use for display, for now we will use first row of file
#defaultArray = None
indexes = [(1, 2)] # indexes to plot data at

freqTodeTuning = lambda x, n: 2*x - 180 if n == 2 or n == 4 else x


fields = ["Mag. Field $I$ (I)", "Pump $I$ (V)", "Pump $\delta$ (MHz)", "Repump $I$ (V)", "Repump $\delta$  (MHz)"]




"""  Kernal Specification 
Notes:
Originally alpha param was set to 1.777e-5 at GaussianProcessRegressor instantiation
    Addition of white kernal allows for noise level optimazation
"""

# pt vs rt
#kernel = RBF(length_scale= [0.252572864, 0., 0.69314718, 0. , 0.69314718]) + \
#         WhiteKernel(noise_level = 1.777e-5)

# pi vs pt
kernel = RBF(length_scale= [0.2, 0.10, 1.0, 0.1, 0.2]) + \
         WhiteKernel(noise_level = 1.777e-5)

try:
    if loadKernelPath:
        kernel = pk.load(open(loadKernelPath, 'rb'))
except Exception as e:
    print("Could not load kernel, useing script default\n\nError:")
    print(e)

fname = join(saveDir, "Kernel-{:}.pkl".format(round(time())))
if saveKernel:
    pl.dump(kernel, open(fname, 'wb'))

def parseData(dataPath, dataTable, refit = True):
    with open(dataTable, 'w') as dataFile:
        for path in glob.glob(join(dataPath, '*.pkl')):
            systemSettings, vt, t, result = pk.load(open(path, 'rb'))
            try:
                if refit:
                    data = np.array([t, vt]).T
                    result, err = fit.fitSample(data, verbose=1)
    
                if result:
                    dataFile.write(", ".join(map(str, systemSettings['params'] + [result[0],result[1],result[2], time(), path]))+'\n')
            except Exception as e:
                print("Error on datapoint:")
                print(systemSettings['params'])
                print("Fit not appended to record.")
                print(e)
            
#        systemSettings, vt, t, result = pk.load(open(path, 'rb'))
#
#        if refit:
#            data = np.array([t, vt]).T
#            result, err = fit.fitSample(data, verbose=1)
#        with open(dataTable, 'a') as dataFile:
#            if result:
#                dataFile.write(", ".join(map(str, systemSettings['params'] + [result[0],result[1],result[2], time(), path]))+'\n')


def fitFile(path, kernel):
    data = np.genfromtxt(path, delimiter = ',', comments='#')
    model = GaussianProcessRegressor(kernel=kernel, normalize_y = True)
    x = data[:,0:5]
    y = data[:,5]
    model.fit(x, y)
    
    fname = join(saveDir, "./Model-{:}.pkl".format(round(time())))
    if saveModel:
        pl.dump([model, (x, y)], open(fname, 'wb'))
        
    return model, (x, y)



def gbSurf(arr, model, a, b, x, y, genError = True): # inefficient, find better solution
    newArr = np.array(arr)
    np.put(newArr, [a, b], [x, y])
    return model.predict(newArr.reshape(1, -1), return_std=genError)

gbSurf = np.vectorize(gbSurf, excluded=[0, 1, 2, 3])

def cmap(z):
    zmin, zmax =  min(z), max(z)

def updateDisplay(indexes, data, default, model, types = ['contour', 'data', 'error']):
    global x, y, z, ctp
    x, y = data

    for (a, b) in indexes:

        # small namespace confusion as we move to 3d
        xmin, xmax =  np.min(x[:,a]), np.max(x[:,a])
        ymin, ymax =  np.min(x[:,b]), np.max(x[:,b])
        
        if not xmax - xmin:
            xmax, xmin = 0.01*1, -0.01*1
            
        if not ymax - ymin:
            ymax, ymin = 0.01 + ymax, -0.01 + ymin
            
        xrng = xmax - xmin
        yrng = ymax - ymin
        
        x, y = np.meshgrid(np.linspace(xmin - xrng*expand, xmax + xrng*expand, nPoints), 
                           np.linspace(ymin - yrng*expand, ymax + yrng*expand, nPoints))
        
        z, err = gbSurf(default, model, a, b, x, y)

        fig = pl.figure() # global figure for updating
        
        if 'contour' in types or  'data' in types or not types:
            pl.contourf(freqTodeTuning(x, a), freqTodeTuning(y, b), z, 8, cmap = cm.Blues)
            ctp = pl.contour(freqTodeTuning(x, a), freqTodeTuning(y, b), z, 8, colors='k')
            pl.clabel(ctp, inline=1, fontsize=10)
            pl.xlabel(fields[a]); pl.ylabel(fields[b]); pl.title("MOT Depth $R_V$", fontsize=16)
            pl.plot(freqTodeTuning(data[0][:,a], a), freqTodeTuning(data[0][:,b], b), 'k.')
            pl.tight_layout()
            pl.savefig('Contour.eps', format = 'eps', dpi=800)
            pl.show()
            
            if 'data' in types:
                #find contour of maximum depth and generate a selction of points from this data
                contourDepths = [gbSurf(default, model, a, b, *p.get_paths()[0].vertices[0])
                                    for p in list(ctp.collections)]
                
#                maxDepths = np.argmax(contourDepths) -1
#                print(maxDepths)
                print(contourDepths)
                
                maxDepths = 1
                with open('isolevel.csv','w') as f:
    #                print("Iso-level data from deepest contour.")
                    print("Iso-level data from countour. {:}".format(maxDepths))
                    print("\n\n{:} \t{:} \t{:}".format(
                          fields[a], 
                          fields[b],
                          "R_v"))
                    
                    
                with open('isolevel.csv','w') as f:
                    f.write("#{:},\t{:},\tRv\t defualt={:}\n".format(fields[a],  fields[b], str(defaultArray)))
                    for n, p in enumerate(ctp.collections[maxDepths].get_paths()[0].vertices):
                        
                        vals = (*p, gbSurf(default, model, a, b, *p)[0][0])
    #                    print("{:1.3e} \t{:1.3e} \t{:1.3e}".format(
                        print("{:1.3f} &{:1.3f} &{:1.3f} \\\\".format(*vals))
                        
                        f.write("{:},\t{:},\t{:}\n".format(*vals))

            
        
        if '3d' in types:   
            ax = fig.gca(projection='3d')  
        
        # interpolate for easier reading, ONLY ENABLE WHEN KERNAL IS OPTIMIZED FOR EXP.
        if interpolate:
            interpObj = interp.bisplrep(x, y, z, s=2)
            xInterp = np.linspace(xmin, xmax, nPoints*upScaleFactor)
            yInterp = np.linspace(ymin, ymax, nPoints*upScaleFactor)
            zInterp = interp.bisplev(xInterp, yInterp, interpObj)
            xInterp, yInterp= np.meshgrid(xInterp, yInterp)
            if '3d' in types: 
                surf = ax.plot_surface(xInterp, yInterp, zInterp, linewidth=0)  
                
        else:
        # non-smoothed alternative
            if '3d' in types:   
                ax.plot_surface(x, y, z, linewidth=0)
    
        if '3d' in types:          
            pl.title('MOT Depth', fontsize=16)
            ax.set_xlabel(fields[a])
            ax.set_ylabel(fields[b])
            ax.set_zlabel("$R_V$")
            pl.tight_layout(pad=0.4)
            
            if 'scatter' in types: 
                ax.scatter(data[0][:,a], data[0][:,b], data[1], zdir='z', s=30, c = 'red')   
                
            ax.plot(data[0][:,a], data[0][:,b], data[1], 'r.') 
            pl.tight_layout()
            pl.savefig('Scatter.eps', format = 'eps', dpi=800)
            pl.show()
        
        
        if 'error' in types:        
            pl.contourf(freqTodeTuning(x, a), freqTodeTuning(y, b), err, cmap=cm.inferno_r)
            pl.title('MOT Depth $\sigma$', fontsize=16)
            pl.xlabel(fields[a])
            pl.ylabel(fields[b])
            pl.colorbar()
            pl.plot(freqTodeTuning(data[0][:,a], a), freqTodeTuning(data[0][:,b], b), 'ro')
            
            # find largest error     
            maxErr = 0
            maxErrPos = None
            for p in data[0]:
                dist = np.hypot(x - p[a], y - p[b])
                errMask = np.ma.masked_where(dist <= 0.1, err)
                pos = np.unravel_index(errMask.argmax(), errMask.shape)
                if maxErr < err[pos]:
                    maxErr = err[pos]
                    maxErrPos = pos
            pl.plot(freqTodeTuning(x[:,maxErrPos[0]][0], a), freqTodeTuning(y[maxErrPos[1],:][0], b), 'bo')
            pl.tight_layout()
            pl.savefig('Error.eps', format = 'eps', dpi=800)
            pl.show()
        
def display(dataTablePath):
    global model, data, defaultArray, kernal

    model, data = fitFile(dataTablePath, kernel)
    if defaultArray is None:
        defaultArray = data[0][0,:]
    updateDisplay(indexes, data, defaultArray, model)

        
# Hashing was excessive, now we just join 
currHash = ""
lastHash = None
def monitor(path):
    global lastHash, currHash
    while True:
        currHash = "\n".join(glob.glob(join(path, './*.pkl')))
    
        if lastHash == currHash: # try again later
            sleep(updateInt)
            continue

        lastHash = currHash # update hash
        try:
            display(dataTablePath)
        except Exception as e:
            print("There was an error displaying the model")      
            print(e)
        
    
if __name__ == '__main__':    
    display(dataTablePath)
