# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:37:08 2017

@author: QDG
"""

from lib.MOt_fpga_class_adc import MOT
from lib import AnalogOutput, DDS
from lib import Recipe, Run
from time import time, localtime, strftime, sleep,asctime
from MOTfpga_class import MOT
import numpy as np
import os
from ADCScriptPE import *
from DefaultSettings import *
from etc.units import *

from PMDController import *
tstart=time()


mot = MOT("MOT_object_1")

mot.makedir()
dname=mot.dname
d=[11]
pref=[2.5]
pref=np.linspace(0.8,2.5,8)

#PMDInterface = MCInput(lowChan = 0,
#                        highChan = 0,
#                        maxDuration = 120,
#                        rate = 200)

startTime=time()

"""MOT Functions"""
# These were previously methods of the mot class
# As such they are only safe to call after INIT
def set_MOT_for_imaging_std(Bfield=True):
    global settings, coil, pump_DDS, repump_DDS, pump_reference
    # Set Magnetic field coil to some standard coil gradient
    if Bfield==True:
        coil.set_scaled_value(settings['MOT_coil_set'])


    # Set MOT detunings and powers to some standard imaging values

    pump_DDS.single_tone(settings['pump_AOM_freq']*MHz)  # MOT Pump frequency
    repump_DDS.single_tone(settings['repump_AOM_freq']*MHz) # repump frequency
    pump_DDS.set_amplitude(settings['pump_ampl'])
    pump_reference(settings['pump_reference'])
    repump_DDS.set_amplitude(settings['repump_DDS.set_amplitude'])


def Pump_shutter(val):
    global pshutter
    if val==1:
        pshutter.set_scaled_value(3)
    else:
        pshutter.set_scaled_value(0)


def Repump_shutter(val):
    global rpshutter
    if val==1:
        rpshutter.set_scaled_value(3)
    else:
        rpshutter.set_scaled_value(0)

for j in range(len(d)):
    for i in range(len(pref)):

        """Begin MOT Class Replacement"""

        """INIT"""
        settings=defaults
        # Prometheus Magnetic Field Control
        coil = AnalogOutput(address = 216)
        #Pump Shutter
        pshutter = AnalogOutput(address = 217)
        #Repump Shutter
        rpshutter = AnalogOutput(address = 218)
        #Trigger
        trigVolts=AnalogOutput(address = 219)
        #Pump reference channel
        pump_ref=AnalogOutput(address = 220)
        # Prometheus DDSs
        # pump_DDS = MOT pump
        # repump_DDS = MOT repump
        pump_DDS=DDS(address= 112, refclock=15*MHz, refclock_multiplier=20,internal_FSK=False)
        repump_DDS=DDS(address= 96, refclock=15*MHz, refclock_multiplier=20,internal_FSK=False)

        #RF DDS
        RFcoil=DDS(address=108, refclock=15*MHz, refclock_multiplier=20,internal_FSK=False)

        R = Recipe("PrometheusExperiment",
                   use_internal_clock=True,
                   sampling_frequency_divider=40,
                   use_external_trigger=False)

        startTime = None

        #External ADC
        PMDInterface = MCInput(lowChan = 0,
                                    highChan = 0,
                                    analoug_range = 1, scale = False,
                                    rate = 200,
                                    maxDuration = 240)

        """Start MOT Recipe"""
        R.start()
        startTime = time()

        """Change Standard Settings"""
        #Std Settings
        settings['pump_AOM_freq']=85
        settings['repump_AOM_freq']=90
        settings['pump_reference']=2.5
        settings['pump_ampl']=0.4
        settings['repump_DDS.set_amplitude']=0.15
        settings['MOT_coil_set']=0.5

        #Test Settings
        settings['test_pump_AOM_freq']=90-d[j]/2
        settings['test_repump_AOM_freq']=90
        settings['test_pump_reference']=pref[i]
        settings['test_pump_ampl']=0.4
        settings['test_repump_DDS.set_amplitude']=0.15
        settings['test_MOT_coil_set']=0.5


        ### initialize MOT, was mot.MOT_initialize()
        pump_DDS.reset()
        repump_DDS.reset()
        R.wait_cycles(500*msec) #let MOT clear

        set_MOT_for_imaging_std(Bfield=False)

        Pump_shutter(1)
        Repump_shutter(1)

        #Standard baseline
        mot.baseline_std()
        #mot.setTrig(4)

        #Pump standard
        Repump_shutter(0)
        R.wait_cycles(mot.settings['wait_pump']*msec)
        #mot.setTrig(0)

        #Repump standard
        Pump_shutter(0)
        pump_ref.set_scaled_value(0)
        Repump_shutter(1)
        R.wait_cycles(mot.settings['wait_repump']*msec)
        #mot.setTrig(4)

        #Load MOT at standard values
        Pump_shutter(1)

        ## load mot, was mot.loadMOT_std()
        coil.set_scaled_value(0)
        mot.set_MOT_for_imaging_std(True)
        R.wait_cycles(mot.settings['wait_Load']*msec)

        #mot.setTrig(0)

        ##Image the MOT at test settings, was mot.image_test()
        mot.set_MOT_for_imaging_test(Bfield=True)
        R.wait_cycles(mot.settings['wait_image']*msec)
        #mot.setTrig(4)


        #Turn off shutters
        Pump_shutter(0)
        pump_ref.set_scaled_value(0)
        Repump_shutter(0)
        R.wait_cycles(mot.settings['wait_background']*msec)
        #mot.setTrig(0)

       #Acquire baseline at test settings
        Pump_shutter(1)
        Repump_shutter(1)
        ## do baseline test, was mot.baseline_test()
        mot.set_MOT_for_imaging_test(Bfield=False)
        coil.set_scaled_value(0)
        R.wait_cycles(mot.settings['wait_baseline']*msec)
        #mot.setTrig(4)

        #Pump test
        Repump_shutter(0)
        R.wait_cycles(mot.settings['wait_pump']*msec)
        #mot.setTrig(0)


        #Repump test
        Pump_shutter(0)
        pump_ref.set_scaled_value(0)
        Repump_shutter(1)
        R.wait_cycles(mot.settings['wait_repump']*msec)
        #mot.setTrig(4)


        #baseline standard
        Pump_shutter(1)
        ## was mot.baseline_std()
        mot.set_MOT_for_imaging_std(Bfield=False)
        coil.set_scaled_value(0)
        R.wait_cycles(mot.settings['wait_baseline']*msec)
        #mot.setTrig(0)

        #Pump std
        Repump_shutter(0)
        R.wait_cycles(mot.settings['wait_pump']*msec)
        #mot.setTrig(4)

        #Repump std
        Pump_shutter(0)
        pump_ref.set_scaled_value(0)
        Repump_shutter(1)
        R.wait_cycles(mot.settings['wait_repump']*msec)
        #mot.setTrig(0)

        pump_DDS.set_amplitude(0)
        pump_ref.set_scaled_value(0)
        repump_DDS.set_amplitude(0)
        Pump_shutter(1)
        Repump_shutter(1)
        coil.set_scaled_value(0)

        setBfield(self.settings['test_MOT_coil_set'])
        R.end()

        """Save Data"""
        Asctime=asctime()
        tstring=Asctime[20:24]+Asctime[4:7]+Asctime[8:10]+'_'+Asctime[11:13]+'.'+Asctime[14:16]+'.'+Asctime[17:19]

        data, s, e = self.capture()
        np.savetxt(self.adc_folder+"/data"+tstring+".csv", data.T,
                   header="Timestamp(usec), Voltage(mV)",
                   newline='\n', delimiter=', ', comments='')

        PMDInterface.captureEvent(duration = time() - self.startTime)

        f=open(self.adc_folder+'/Settings'+tstring+'.txt','w')
        f.write(str(self.settings))
        f.close()
