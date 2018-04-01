#!/usr/bin/env python
#title           :MOT_fpga_class_adc.py
#description     : Displays the Gaussian process model and update continously
#author          :
#email           :
#date            :09.01.2018
#version         :2
#notes           :
#python_version  :3.6
#==============================================================================

from __future__ import print_function
from analysis.gaussianProcess import *
import time, glob, time,  os

# Hashing was excessive, now we just join paths
currHash = None 
lastHash = None

dataTablePath = './fitData.csv' # path to for data fitting
dataPath = './MOTData' # path to for data fitting

def monitor(path, persistent = True):
    global lastHash, currHash
    while persistent or currHash is None:
        
        if not os.path.exists(dataTablePath):
            print("Update")
            parseData(dataPath, dataTablePath)
        
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
        monitor(dataTablePath, persistent = False)
