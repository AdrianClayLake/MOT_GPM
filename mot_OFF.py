# -*- coding: utf-8 -*-
# title           :mot_ON.py
# description     :Enable MOT undefnitly 
# author          :Adrian Lake
# email           :
# date            :09.01.2018
# version         :1
# usage           :
# notes           :This script still has to be converted to a non mot class version but its function is simple and non vital to data collection, low priority
# python_version  :
#==============================================================================



from lib.MOt_fpga_class_adc import MOT
import lib.Run
from etc.units

UTBusClock = 0.5*MHz # Frequency of the External Clock into UT Bus REQ input; This is standard from DDS #28. This can be changed if necessary, or run on the internal clock.

sec  = 10**6 # 1 wait cycle is equal to the Inverse of the External Clock
msec = sec/1e3
mot = MOT("MOT_object_1")

mot.start() 
mot.settings['pump_reference']=0
mot.pump_reference(mot.settings['pump_reference'])
mot.Repump_ampl(0)
mot.Pump_ampl(0)
mot.settings['MOT_coil_set']=0
mot.settings['test_MOT_coil_set']=0
mot.setBfield(0)
mot.Pump_shutter(1)
mot.Repump_shutter(1)
           
mot.end()
Run.run()
            

