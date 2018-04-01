#!/usr/bin/env python
#title           :MOTControl.py
#description     :Samples MOT for TDS study
#author          :Adrian Lake
#email           :clake95@gmail.com
#date            :09.01.2018
#version         :1
#usage           :python ADCScript.py
#notes           :The code below was built off of other peoples scripts,  it may contain extrenious operations
#python_version  :3.6 (Tested)
#==============================================================================



from MOT_fpga_class_adc import MOT

import numpy as np
from time import time as time
import Run
from PMDController import *

# units/scales
KHz = 1.0e3
MHz = 1.0e6
sec  = 1000000 # 1 wait cycle is equal to the Inverse of the External Clock
msec = sec*1.0e-3
UTBusClock = 0.5*MHz # Frequency of the External Clock into UT Bus REQ input; This is standard from DDS #28. This can be changed if necessary, or run on the internal clock.



def sampleMOT(b, pi, pt, ri, rt):
    # Samples MOT according to TDS
    mot = MOT("MOT_object_1")
    mot.start()

    mot.settings['wait_pump']=5000
    mot.settings['wait_baseline']=5000
    mot.settings['wait_Load']=30000
    mot.settings['wait_image']=5000

    #Std Settings
    mot.settings['pump_AOM_freq']=85
    mot.settings['repump_AOM_freq']=90
    mot.settings['pump_reference']=2.5
    mot.settings['pump_ampl']=0.4
    mot.settings['repump_ampl']=0.15
    mot.settings['MOT_coil_set']=0.5

    #Test Settings
    mot.settings['test_pump_AOM_freq']=pt
    mot.settings['test_repump_AOM_freq']=rt
    mot.settings['test_pump_reference']=pi
    mot.settings['test_pump_ampl']=0.4 # This is fixed, max power for AOM
    mot.settings['test_repump_ampl']=ri
    mot.settings['test_MOT_coil_set']=b

    #Initialize
    #mot.setTrig(0)
    mot.MOT_initialize()

    #Pump test
    mot.Repump_shutter(0)
    mot.baseline_test()

    #Baseline test
    mot.Repump_shutter(1)
    mot.baseline_test()

    #Load MOT at test values
    mot.loadMOT_test()
    #mot.setTrig(0)

    #Image the MOT at std settings
    mot.image_std()
    #mot.setTrig(4)

    #Acquire baseline at std settings
    mot.baseline_std()
    #mot.setTrig(4)

    #Turn off Repump
    mot.Repump_shutter(0)
    mot.R.wait_cycles(mot.settings['wait_pump']*msec)
    #mot.setTrig(0)

    mot.Pump_ampl(0)
    mot.pump_reference(0)
    mot.Repump_ampl(0)
    mot.Pump_shutter(1)
    mot.Repump_shutter(1)
    mot.setBfield(0)

    mot.end() # end
    (t, vt), s, e = mot.capture()
    return t, vt, mot.settings


if __name__ == '__main__':
    """Example for debugging"""
    import matplotlib.pyplot as pl
    x, y, settings = sampleMOT(0.5, 0.4, 85, 0.15 , 90)
    print('x:', x)
    print('y:', y)
    pl.plot(x, y)
