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


from math import sin,cos
import socket
import sys

from lib import AnalogOutput, DigitalOutput, DDS
from lib import Recipe

import math as mth
from time import time, localtime, strftime, sleep,asctime
import numpy as np
import os
import Run
from ADCScriptPE import *

from DefaultSettings import *

KHz = 1000.
MHz = 1000000.

UTBusClock = 0.5*MHz # Frequency of the External Clock into UT Bus REQ input; This is standard from DDS #28. This can be changed if necessary, or run on the internal clock.

sec  = 1000000 # 1 wait cycle is equal to the Inverse of the External Clock
msec = sec/1000.


class MOT:

    # Constructor
    def __init__(self, name):
        self.name = name
        self.settings=defaults
        # Prometheus Magnetic Field Control
        self.coil = AnalogOutput(address = 216)

        #Pump Shutter
        self.pshutter = AnalogOutput(address = 217)
        #Repump Shutter
        self.rpshutter = AnalogOutput(address = 218)


        #Trigger
        self.trigVolts=AnalogOutput(address = 219)

        #Pump reference channel
        self.pump_ref=AnalogOutput(address = 220)

        # Prometheus DDSs
        # pump_DDS = MOT pump
        # repump_DDS = MOT repump
        self.pump_DDS=DDS(address= 112, refclock=15*MHz, refclock_multiplier=20,internal_FSK=False)
        self.repump_DDS=DDS(address= 96, refclock=15*MHz, refclock_multiplier=20,internal_FSK=False)

        #RF DDS
        self.RFcoil=DDS(address=108, refclock=15*MHz, refclock_multiplier=20,internal_FSK=False)

        self.R = Recipe("PrometheusExperiment",
                   use_internal_clock=True,
                   sampling_frequency_divider=40,
                   use_external_trigger=False)


        self.startTime = None
        
        #External ADC
        self.PMDInterface = MCInput(lowChan = 0,
                                    highChan = 0,
                                    analoug_range = 1, scale = False,
                                    rate = 200,
                                    maxDuration = 240)

    def pump_reference(self,val):
        self.pump_ref.set_scaled_value(val)

    def pump_power(self,power):
        voltage=power*0.1258-0.0272 #Convert voltage to power
        self.pump_ref.set_scaled_value(voltage)


    def set_MOT_for_imaging_std(self,Bfield=True):
        # Set Magnetic field coil to some standard coil gradient
        if Bfield==True:
            self.coil.set_scaled_value(self.settings['MOT_coil_set'])


        # Set MOT detunings and powers to some standard imaging values

        self.pump_DDS.single_tone(self.settings['pump_AOM_freq']*MHz)  # MOT Pump frequency   
        self.repump_DDS.single_tone(self.settings['repump_AOM_freq']*MHz) # repump frequency
        self.pump_DDS.set_amplitude(self.settings['pump_ampl'])
        self.pump_reference(self.settings['pump_reference'])
        self.repump_DDS.set_amplitude(self.settings['repump_ampl'])

    def set_MOT_for_imaging_test(self,Bfield=True):
        # Set Magnetic field coil to some standard coil gradient
        if Bfield==True:
            self.coil.set_scaled_value(self.settings['test_MOT_coil_set'])


        # Set MOT detunings and powers to some standard imaging values

        self.pump_DDS.single_tone(self.settings['test_pump_AOM_freq']*MHz)  # MOT Pump frequency
        self.repump_DDS.single_tone(self.settings['test_repump_AOM_freq']*MHz) # repump frequency
        self.pump_DDS.set_amplitude(self.settings['test_pump_ampl']) #turn on AOMs
        self.repump_DDS.set_amplitude(self.settings['test_repump_ampl'])


    def MOT_initialize(self):
        # initialize MOT
        self.pump_DDS.reset()
        self.repump_DDS.reset()
        #self.DO0.set_bit(10,1) # trigger- set high
        self.R.wait_cycles(500*msec) #let MOT clear

        self.set_MOT_for_imaging_std(Bfield=False)

        self.Pump_shutter(1)
        self.Repump_shutter(1)

    def Pump_shutter(self,val):
        if val==1:
            self.pshutter.set_scaled_value(3)
        else:
            self.pshutter.set_scaled_value(0)



    def Repump_shutter(self,val):
        if val==1:
            self.rpshutter.set_scaled_value(3)
        else:
            self.rpshutter.set_scaled_value(0)

    def Cooling(self, val):
        if val==True:
            cooling_frequency=(180.0-defaults['detuning'])/2*MHz
            self.pump_DDS.single_tone(cooling_frequency)
            self.pump_DDS.set_amplitude(0.9)#0.9
            self.repump_DDS.set_amplitude(0.1)#0.9
            self.R.wait_cycles(defaults['wait_cool']*msec)

    #AOM functionality
    def Pump_ampl(self,val):
        self.pump_DDS.set_amplitude(val)

    def Repump_ampl(self,val):
        self.repump_DDS.set_amplitude(val)


    def Pump_freq(self,val):
        self.pump_DDS.single_tone(val)

    def Repump_freq(self,val):
        self.repump_DDS.single_tone(val)


    def setBfield(self,val):
        self.coil.set_scaled_value(val)

    def Check_Fstate(self,val):
        if val==2:
            #Hyperfine Pumping to F=2
            self.Pump_shutter(0)
            self.Pump_ampl(0)
            self.pump_reference(0)
            self.R.wait_cycles(defaults['wait_hfine_pump_F2']*msec)
            self.Repump_shutter(0)
            self.Repump_ampl(0)
            self.setBfield(2.0) #Gravitationally Filter out MF=2 state
            self.R.wait_cycles(50.0*msec)

        else:
            #Hyperfine Pumping to F=1
            self.Repump_shutter(0)
            self.Repump_ampl(0)
            self.R.wait_cycles(defaults['wait_hfine_pump_F1']*msec)
            self.Pump_shutter(0)
            self.pump_reference(0)
            self.Pump_ampl(0)

    def RF_slice(self,amplitude,time,fmin,fmax):
        self.RFcoil.set_amplitude(amplitude)
        self.RFcoil.triangle_ramp(fmin*MHz,fmax*MHz,0.000517) #sweeprate=0.000517
        self.R.wait_cycles(time*msec)
        self.RFcoil.set_amplitude(0)

    def loadMOT_std(self):
        self.setBfield(0)
        self.set_MOT_for_imaging_std(True)
        self.R.wait_cycles(self.settings['wait_Load']*msec)
        
    def loadMOT_test(self):
        self.setBfield(0)
        self.set_MOT_for_imaging_test(True)
        self.R.wait_cycles(self.settings['wait_Load']*msec)

    def mTrap_for_time(self):
        self.setBfield(self.settings['coil_set'])   #Turn on magnetic trap at current coil set
        self.set_MOT_for_imaging_std(Bfield=False) #Turn off DDS, but don't change magnetic field

 
        self.R.wait_cycles(self.settings['wait_mtrap']*msec-self.settings['dtpump']*msec-self.settings['dtrepump']*msec-self.settings['RFtime'])
        print(self.settings['wait_mtrap']*msec-self.settings['dtpump']*msec-self.settings['dtrepump']*msec-self.settings['RFtime'])
        self.RF_slice(self.settings['RFampl'],
                    self.settings['RFtime'], 
                    self.settings['fmin'],
                    self.settings['fmax'])  

        #Turn off AOMs again
        self.pump_reference(0)
        self.Pump_ampl(0)
        self.Repump_ampl(0)
        self.Repump_shutter(1)
        self.R.wait_cycles(self.settings['dtrepump']*msec) 
        self.Pump_shutter(1)



        self.R.wait_cycles(self.settings['dtpump']*msec)
     
    def image_std(self):
        self.set_MOT_for_imaging_std(Bfield=True)
        self.R.wait_cycles(self.settings['wait_image']*msec)
        
    def image_test(self):
        self.set_MOT_for_imaging_test(Bfield=True)
        self.R.wait_cycles(self.settings['wait_image']*msec)       
        
    def baseline_std(self):
        self.set_MOT_for_imaging_std(Bfield=False)
        self.setBfield(0)
        self.R.wait_cycles(self.settings['wait_baseline']*msec)

    def baseline_test(self):
        self.set_MOT_for_imaging_test(Bfield=False)
        self.setBfield(0)
        self.R.wait_cycles(self.settings['wait_baseline']*msec)

    def start(self):
        self.R.start()
        self.startTime = time()

    def end(self):
        self.setBfield(self.settings['test_MOT_coil_set'])
        self.R.end()


    def makedir(self):
        Asctime=asctime()
        tstring=Asctime[20:24]+Asctime[4:7]+Asctime[8:10]+'_'+Asctime[11:13]+'.'+Asctime[14:16]+'.'+Asctime[17:19]
#        self.dname='./MOT_Data/MOTfpga_data'+tstring
#        os.makedirs(self.dname)
        self.adc_folder='./MOT_Data/MOTfpga_adc'+tstring
        os.makedirs(self.adc_folder)


    def capture(self):
        self.PMDInterface.start()
            
        self.times = Run.run()
        
        return self.PMDInterface.stop()

    def SaveData(self):
        Asctime=asctime()
        tstring=Asctime[20:24]+Asctime[4:7]+Asctime[8:10]+'_'+Asctime[11:13]+'.'+Asctime[14:16]+'.'+Asctime[17:19]
        
        data, s, e = self.capture()
        np.savetxt(self.adc_folder+"/data"+tstring+".csv", data.T, 
                   header="Timestamp(usec), Voltage(mV)", 
                   newline='\n', delimiter=', ', comments='')

        self.PMDInterface.captureEvent(duration = time() - self.startTime)

        f=open(self.adc_folder+'/Settings'+tstring+'.txt','w')
        f.write(str(self.settings))
        f.close()

           