#!/usr/bin/env python
#title           :manualControl.py
#description     :Workspace for manual manipulation of MOT
#author          :
#email           :
#date            :09.01.2018
#version         :2
#notes           :
#python_version  :3.6 (Tested)
#==============================================================================
from __future__ import print_function

import socket
import sys

from lib import AnalogOutput, DigitalOutput, DDS
from lib import Recipe
from etc.units import *
from lib import Run


motOnState = (0.5, 0.8, 85.0, 0.15, 90.0, True, True)
motOffState = (0.0, 0.0, 0.0, 0.0, 0.0, False, False)
state = motOff


dispFmt = """MOT State:
    Coils \t=> {:}
    Pump Volt. \t=> {:}
    Pump Freq. \t=> {:}
    Repump Volt. \t=> {:}
    Repump Freq. \t=> {:}
    Shutter 1 \t=> {:}
    Shutter 2 \t=> {:}
"""

def disp():
    print(dispFmt.format(*state))

def zeroAll():
    setState(0.0, 0.0, 0.0, 0.0, 0.0, True, True)
    disp()

def motOff():
    setState(*motOffState)
    disp()

def motOn():
    setState(*motOnState)
    disp()

def setMOT(b = None,
           pi = None, pt = None,
           ri = None, rt = None,
           s1 = None, s2 = None, quiet = False):
            global state

            # update global state
            for n, p in enumerate([b, pi, pt, ri, rt, s1, s2]):
               if not p is None:
                   state[n] = p

            # get all parameter values
            b, pi, pt, ri, rt, s1, s2 = state


            # follow general routine for setting MOT state
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

            # DDS initialization
            pump_DDS.reset()
            repump_DDS.reset()
            pump_DDS.single_tone(pt*MHz)
            pump_DDS.set_amplitude(pi)
            pump_intensity_ref.set_scaled_value(1.8) # TODO: What is this?
            repump_DDS.single_tone(rt*MHz)
            repump_DDS.set_amplitude(ri)
            MOT_coil.set_scaled_value(0.0) # TODO: What is this?
            pump_shutter.set_scaled_value(3.0 if s1 else 0.0)
            repump_shutter.set_scaled_value(3.0 if s1 else 0.0)
            analog_trigger.set_scaled_value(0.0) # TODO: What is this?


            def pump_reference(val):
                if (val < 0) or (val > 5):
                raise Exception ("pump_reference value is '%f' and out of range [0,5]" % val)
                pump_intensity_ref.set_scaled_value(val)

            pump_reference(6.0)  # TODO: What is this?

            R.end()
            Run.run()

            if not quiet:
                print("MOT update successful")
                disp()

def setState(b, pi, pt, ri, rt, s1, s2):
    setMOT(b-b, pi=pi, pt=pt, ri=ri, rt=rt, s1=s1, s2=s2)


motOff()
