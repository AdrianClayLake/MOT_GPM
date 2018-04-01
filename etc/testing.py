#!/usr/bin/env python
#title           :testing.py
#description     :Test cases for development
#author          :
#email           :
#date            :09.01.2018
#version         :2
#notes           :
#python_version  :3.6 (Tested)
#==============================================================================

testPaths = ['./etc/data2017Sep20_11.50.35.csv',
             './etc/data2017Sep20_11.48.43.csv',
             './etc/data2017Sep20_11.46.52.csv',
             './etc/data2017Sep20_11.45.00.csv',
             './etc/data2017Sep20_11.43.08.csv']

#for p in paths:
#    data = np.genfromtxt(p, delimiter = ',', comments='#', skip_header=1)
#    results, error = fit(data)
#    print "{:}\n\t{:}\n".format(p, results)

def testLoop():
    from time import sleep
    while True:
        print("Loaded")
        sleep(1)
