#!/usr/bin/env python
#title           :DefaultSettings.py
#description     :Defualt MOT settings
#author          :
#email           :
#date            :09.01.2018
#version         :2
#notes           :
#python_version  :3.6 (Tested)
#==============================================================================
defaults={
        #Cooling Settings
        'detuning':30.,
        'wait_cool':0,
        'bool_cooling':True,

        #Timing Settings
        'wait_image':2000, #image time
        'wait_Load':40000,#loading time
        'wait_hfine_pump_F1':2,
        'wait_hfine_pump_F2':2,
        'wait_baseline':5000, #baseline time

        #Shutter timing settings
        'dtpump':2.1, #time to open pump shutter
        'dtrepump':0.6, #time to open repump shutter

        # Trap settings
        'coil_set':6.0, #coil current when mtrap (A)
        'wait_mtrap':5000, #time for magnetic trap

        #Image MOT Settings
        'MOT_coil_set':0.5,#coil current when both light and Bfield on (A)
        'pump_AOM_freq' :85,
        'repump_AOM_freq' : 90,
        'pump_ampl' : 0.4,
        'repump_ampl' : 0.16,
        'pump_reference' : 1.8, #control voltage (V)

        #RF Settings
        'RFtime':50,
        'fmin':80,
        'fmax':140,
        'RFampl':1,

        #Analysis times
        'wait_pump':5000, #time for pump scattering light
        'wait_repump':5000, #time for repump scattering light
        'load_linfit_1':3000, #time to linearly fit the start part of the loading curve
        'load_linfit_2':5000, #time to linearly fit the end part of the loading curve
        'wait_background':1000, #time for backgound light

        #Test Settings
        'test_coil_set':6.0,#1.1, #6.0,
        'test_MOT_coil_set':0.5, #1.1,
        'test_pump_AOM_freq' : 85, #86,#85,
        'test_repump_AOM_freq' : 90,
        'test_pump_ampl' : 0.4,#0.4, #0.55,
        'test_repump_ampl' : 0.16,
        'test_pump_reference' : 1.8#1.5    
}
