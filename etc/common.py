#!/usr/bin/env python
#title           :common.py
#description     :header of units and other small details
#author          :Adrian Lake
#email           :clake95@gmail.com
#date            :09.01.2018
#version         :1
#usage           :python ADCScript.py
#notes           :The code below was built off of other peoples scripts, it may contain extrenious operations
#python_version  :3.6 (Tested)
#==============================================================================

KHz = 1.0e3
MHz = 1.0e6
sec  = 10**6 # 1 wait cycle is equal to the Inverse of the External Clock
msec = sec*1.0e-3
UTBusClock = 0.5*MHz # Frequency of the External Clock into UT Bus REQ input; This is standard from DDS #28. This can be changed if necessary, or run on the internal clock.
