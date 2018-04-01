#!/usr/bin/env python
#title           :dataPrescriptionGenerator.py
#description     :
#author          :
#email           :
#date            :09.01.2018
#version         :2
#notes           :
#python_version  :3.6 (Tested)
#==============================================================================

from numpy import linspace

# convert turning to aom freq and back
fToDelta = lambda f: -180.0 + 2.0*f
deltaTof = lambda d: (d + 180.0)/2

# Defaults
a, b, c, d, e = [0.5], [2.5], [85], [0.6], [90]
fname = 'samplePrescription .csv' # default file of sample parameters
append = False # append to fname
a = linspace(0.2, 0.5, 9) # B-feild
b = linspace(0.1, 0.5, 9) # pump intensity
c = linspace(deltaTof(0), deltaTof(20), 9) # pump aom freq
d = linspace(0.1, 0.5, 9) # repump intensity
e = linspace(deltaTof(5), deltaTof(15), 9) # repump aomfreq

header = "#B Feild, Pump Intensity, Pump Tuning, Re-Pump Intensity, Re-Pump Tuning"
with open(fname, 'a' if append else 'w') as f:
    f.write(header + '\n')
    for _a in a:
        for _b in b:
            for _c in c:
                for _d in d:
                    for _e in e:
                        f.write('{:}, {:}, {:}, {:}, {:}\n'.format(a_, b_, c_, d_, e_))
