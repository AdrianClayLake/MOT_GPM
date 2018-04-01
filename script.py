# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 02:25:22 2018

@author: Adrian
"""


error = []
with open('./Verification_fitData.csv','r') as f:
    for l in f.readlines():
        vals = l.split(', ')
        newArr = np.array(gp.defaultArray)
        params = list(map(float, [vals[2], vals[4], vals[0]]))
#        params = list(map(float, [88., 88., 0.4]))
        np.put(newArr, indexes[0],  params)
        realdepth = float(vals[5])
        print(realdepth, params)
        pre, err = model.predict(newArr.reshape(1, -1), return_std=True)
        print(pre, err)
        print()
        error.append(abs(pre-realdepth))
        
        
error = np.array(error).T[0]

pl.hist(error)
pl.xlabel("Absolute Error Vaue")
pl.ylabel("Count")
pl.title("Error Historgram")