# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 12:38:18 2017

@author: QDG
"""

from MOTfpga_class import MOT
import numpy as np
from time import time as time
from time import localtime, strftime, sleep,asctime
import Run

from MOT_data_class import MOT_plot

tstart=time()

KHz = 1000.
MHz = 1000000.

UTBusClock = 0.5*MHz # Frequency of the External Clock into UT Bus REQ input; This is standard from DDS #28. This can be changed if necessary, or run on the internal clock.

sec  = 1000000 # 1 wait cycle is equal to the Inverse of the External Clock
msec = sec/1000.
mot = MOT("MOT_object_1")

## optimal settings (23.11.17)
#d=[87]
#rd=[98]


#d=np.arange(80,88,1)
d=[85] # normal 85  (23.11.17)
#d=[87.85-15/2] #87.85-8/2
#rd=[82] 
rd=[90] #96 # normal 90 (23.11.17)
#rd=np.arange(78,83,1)
#for i in range(len(d)):
#    for j in range (len(rd)):
mot.start()
mot.setBfield(0)
mot.Repump_shutter(1)
mot.Pump_shutter(1)

mot.settings['wait_image']=500
mot.settings['wait_Load']=10000
mot.settings['pump_AOM_freq']=d[0]
mot.settings['repump_AOM_freq']=rd[0]
mot.settings['MOT_coil_set']=0.5
mot.settings['test_MOT_coil_set']=0.5
mot.settings['repump_ampl']=0.1   #0.4
mot.settings['pump_ampl']=0.4 #0.3
mot.settings['pump_reference']=2.5

mot.MOT_initialize()

mot.Repump_ampl(mot.settings['repump_ampl'])
mot.Pump_ampl(mot.settings['pump_ampl'])
mot.pump_reference(mot.settings['pump_reference'])
mot.Pump_freq(mot.settings['pump_AOM_freq']*MHz)
mot.Repump_freq(mot.settings['repump_AOM_freq']*MHz)

mot.baseline_std()

#Optimize detuning

a=0           
for i in range(len(d)):
    for j in range (len(rd)):                   
            mot.loadMOT_std()

#mot.Pump_shutter(0)
#mot.Repump_shutter(0)
#mot.pump_reference(0)
#mot.Repump_ampl(0)
#mot.R.wait_cycles(2*sec)
            
#mot.repump_DDS.triangle_ramp(80*MHz,90*MHz,1.000)
#mot.pump_DDS.triangle_ramp(80*MHz,86*MHz,5.000)
            
mot.end()
#Run.run('./MOT_Data/mot_ON/mot_ON_'+str(d[i])+' '+str(rd[j])+'.csv')
#fluo=MOT_fluo('./MOT_Data/mot_ON','mot_ON_'+str(d[i])+' '+str(rd[j])+'.csv')

Run.run('./MOT_Data/mot_ON/mot_ON_compare.csv')
fluo=MOT_plot('./MOT_Data/mot_ON','mot_ON_compare.csv')
            

##Switch off
#mot.Pump_ampl(0)
#mot.Repump_ampl(0)
#mot.Pump_shutter(1)
#mot.Repump_shutter(1)

