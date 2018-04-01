#!/usr/bin/env python
#title           :MOTControl.py
#description     :Dummy sample function
#author          :Adrian Lake
#email           :clake95@gmail.com
#date            :09.01.2018
#version         :1
#usage           :python ADCScript.py
#notes           :ns
#python_version  :3.6 (Tested)
#==============================================================================

from lib import AnalogOutput, DigitalOutput, DDS
from lib import Recipe
import Run
from ADCScriptPE import *
from PMDController import *

from DefaultSettings import *
from MOTConfig import adress
from MOTConfig import config as motConfig
from ADCConfig import config as adcConfig
from etc.units import *


"""MOT MACROS"""
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
    pshutter.set_scaled_value(3 if val else 0)


def Repump_shutter(val):
    global rpshutter
    rpshutter.set_scaled_value(3 if val else 0)

def wait(ms):
    global R
    R.wait_cycles(mot.settings['wait_repump']*ms)


def sampleMOT(params):

    """BEGIN: INIT"""
    settings=defaults
    # Prometheus Magnetic Field Control
    coil = AnalogOutput(address = address['coil'])
    #Pump Shutter
    pshutter = AnalogOutput(address = address['pshutter'])
    #Repump Shutter
    rpshutter = AnalogOutput(address = address['rpshutter'])
    #Trigger
    trigVolts=AnalogOutput(address = address['trigVolts'])
    #Pump reference channel
    pump_ref=AnalogOutput(address = address['pump_ref'])
    # Prometheus DDSs

    # pump_DDS = MOT pump
    pump_DDS=DDS(address= address['pump_DDS'],
                refclock=motConfig['refclock'],
                refclock_multiplier=motConfig['refclock_multiplier'],
                internal_FSK=motConfig['internal_FSK'])
    # repump_DDS = MOT repump
    repump_DDS=DDS(address= address['repump_DDS'],
                refclock=motConfig['refclock'],
                refclock_multiplier=motConfig['refclock_multiplier'],
                internal_FSK=motConfig['internal_FSK'])
    #RF DDS
    RFcoil=DDS(address=address['RFcoil'],
                refclock=motConfig['refclock'],
                refclock_multiplier=motConfig['refclock_multiplier'],
                internal_FSK=motConfig['internal_FSK'])


    R = Recipe("PrometheusExperiment",
               use_internal_clock=motConfig['use_internal_clock'],
               sampling_frequency_divider=motConfig['sampling_frequency_divider'],
               use_external_trigger=motConfig['use_external_trigger'])

    #External ADC
    PMDInterface = MCInput(lowChan = adcConfig['use_external_trigger'],
                                highChan = adcConfig['use_external_trigger'],
                                analoug_range = adcConfig['use_external_trigger'],
                                scale = adcConfig['use_external_trigger'],
                                rate = adcConfig['use_external_trigger'],
                                maxDuration = adcConfig['use_external_trigger'])

    pump_DDS.reset()
    repump_DDS.reset()
    """END: INIT"""




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



    R.start()
    """BEGIN: SAMPLE ROUTINE"""

    #Example Commands
    # Repump_shutter(0)
    # Pump_shutter(0)
    # set_MOT_for_imaging_std(Bfield=False)
    # wait(100)
    # coil.set_scaled_value(0)
    # pump_DDS.set_amplitude(0)
    # pump_ref.set_scaled_value(0)
    # repump_DDS.set_amplitude(0)
    # repump_ref.set_scaled_value(0)


    """END: SAMPLE ROUTINE"""
    R.end()

    sPMDInterface.start()
    times = Run.run()
    data, s, e = PMDInterface.stop()

    return data, settings



if __name__ == '__main__':
    """Example for debugging"""
    import matplotlib.pyplot as pl
    x, y, settings = sampleMOT(1)
    print('x:', x)
    print('y:', y)
    pl.plot(x, y)
