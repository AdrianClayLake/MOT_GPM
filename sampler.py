# -*- coding: utf-8 -*-
# title           :MOTControl.py
# description     :Samples MOT for TDS study
# author          :Adrian Lake
# email           :clake95@gmail.com
# date            :09.01.2018
# version         :1
# usage           :python ADCScript.py
# notes           :Make sure previous sample data has been removed
# python_version  :3.6 (Tested)
#==============================================================================

# Issues using TkAgg, reverting to Qt of Spyder w/ Py2.7
from __future__ import print_function
import os
from item import time
from shutil import copy
import sys
dryRun = False # does not interact with MOT on dry Run
dataPath = './MOTData' # current sample set
dataSets = './MOTSets' # previous Sample Sets


# set cwd before importing other modules
os.chdir(os.path.dirname(__file__))  # switch to dir of script

import etc.mobileAlert as mobileAlert
from dataSetGenerator import *
import numpy as np
import pickle as pk
from time import sleep, time
from etc.testing import *
import glob

# routine for sampleing MOT, change as needed
if not dryRun:
    import recipes.depth
    sampleMOT = recipes.depth.sampleMOT
import analysis.depthFit as fit

coolDown = 10 if not dryRun else 0  # seconds

# TODO
# grab time that the mot was turned on from RUN
# figureout how to pass data to the sample program
# fit data in fit script
# figure out how to determine if

fields = ["B field", "Pump inten.", "Pump tuning",
          "Repump inten.", "Repump tuning"]


def sample(params, verbose=1):
    global data, fileName
    print("Sampling MOT with parameters:")
    for key, val in zip(fields, params):
        print("\t{:} -> {:1.2f}".format(key, val))

    result, t, vt, settings = None, [], [], {}

    if dryRun:
        # Select test data randomly for fitting
        path = np.random.choice(testPaths)
        t, vt = np.genfromtxt(path, delimiter=',',
                              comments='#', skip_header=1, unpack=True)
        settings = {}  # test parameters
    else:
        # Exdecute Expariment
        t, vt, settings = sampleMOT(*params)  # collect Data

    # Create param dict for pkl
    systemParams = {'params': params, 'settings': settings, 'time': time()}

    # Attempt a fit, alert user if fail
    data = np.array([t, vt]).T
    results, error = fit.fitSample(data, verbose=verbose)
    result = results[0]

    # Save data for later
    fileName = os.path.join(dataPath, fnameFormat(*params))
    with open(fileName, 'wb') as dumpFile:
        pk.dump([systemParams, vt, t, result], dumpFile)
    # add new data to the restults csv
    parseData(fileName)
    return 0


if __name__ == '__main__':
    # remove old files
    for f in glob.glob(os.path.join(dataPath, '*.pkl')):
        os.remove(f)

    if dryRun:
        try:
            with open(dataTablePath, 'w') as dataFile:
                pass
            sleep(1)
        except KeyboardInterrupt:
            print("Data Collection Aborted!")
            sys.exit()

    # Start the GPR preview window


    while scheduledSamples:
        sample(scheduledSamples.pop())  # run a sample in the MOT
        sleep(coolDown)  # Time interval between MOTs

    print('Sampling Complete!!')
    if not dryRun:

        # copy current sample to DataSet Paths
        dirName = datetime.datetime.now().strftime("SampleSet_%Y.%m.%d_%H.%M.%S")
        path = os.makedir(os.path.join(dataSet, dirName)) # relative path
        os.path.join(dataSet, dirName)
        mobileAlert('Sampling Complete!!')

        # Copy samples
        for f in glob.glob(os.path.join(dataPath, '*.pkl')):
            copy(f, path)

        copy(dataTablePath, path) # copy fits
