#!/usr/bin/env python
#title           :MOT_fpga_class_adc.py
#description     : Generate a gaussian process regression model and save
#author          :
#email           :
#date            :09.01.2018
#version         :2
#notes           :
#python_version  :3.6
#==============================================================================

# TODO:
# Make defualt vector constant on lines 42 and 88

from __future__ import print_function
from analysis import gaussianProcess as gp
from skimage.measure import marching_cubes_lewiner
import numpy as np
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import time, glob, time,  os
import pickle


level = 0.008
indexes = [(1, 2, 0)]

"""Get Model and generate isoSurface"""
model, data = gp.fitFile(gp.dataTablePath, gp.kernel)
# Expand model over all valid regions

size = 50
x_min, x_max = 0.09, 0.28
y_min, y_max = 82., 88.
z_min, z_max = 0.2, 1.0

_x = np.linspace(x_min, x_max, size)
_y = np.linspace(y_min, y_max, size)
_z = np.linspace(z_min, z_max, size)
x, y = grid = np.meshgrid(_x, _y )

d = np.array([gp.gbSurf([z, 1.9, 88.0, 0.22, 90.0], model, 
                     indexes[0][0], indexes[0][1], x, y, genError = False) for z in _z])

print("Generating iso-surfaces...")
verts, faces, normals, values = res = marching_cubes_lewiner(d, level)
print("Done")


"""Plot Iso-surface"""
fig = pl.figure()
ax = fig.add_subplot(111, projection='3d')

#AOM frequincy
scaleAOM = np.array([(x_max - x_min)/size, 
                  (y_max - y_min)/size, 
                  (z_max - z_min)/size])
offsetAOM = np.array([x_min, y_min, z_min])


#Detuining freq
scale = np.array([2*(x_max - x_min)/(size-1), 
                      2*(y_max - y_min)/(size-1), 
                      (z_max - z_min)/(size-1)])
offset = np.array([2*x_min - 180, 2*y_min - 180, z_min])

# Fancy indexing: `verts[faces]` to generate a collection of triangles

params = scale*verts[faces] + offset
paramsAOM = scaleAOM*verts[faces] + offsetAOM

mesh = Poly3DCollection(params)
mesh.set_edgecolor('k') 
mesh.set_linewidth(0.1)

ax.add_collection3d(mesh)
ax.set_xlabel(gp.fields[indexes[0][0]])
ax.set_ylabel(gp.fields[indexes[0][1]])
ax.set_zlabel(gp.fields[indexes[0][2]])

ax.set_xlim(x_min*2 - 180, x_max*2 - 180)
ax.set_ylim(y_min*2 - 180, y_max*2 - 180)
ax.set_zlim(z_min, z_max)

fname = '3dContuour'
pl.savefig(fname+'.eps', bbox_inches = 'tight')
pl.savefig(fname+'.png', bbox_inches = 'tight')

pl.show()

errors = []
paramsAOM = paramsAOM.reshape(-1, 3)
for p in paramsAOM:
    newArr = np.array(gp.defaultArray)
    np.put(newArr, indexes[0],  p)
    errors.append(model.predict(newArr.reshape(1, -1), return_std=True))
    
errors = np.array(errors).reshape(-1, 2)
arg_errors = np.argsort(errors[:, 1])

print("\n\n{:} \t{:} \t{:} \t{:}".format(gp.fields[indexes[0][0]],
      gp.fields[indexes[0][1]], 
      gp.fields[indexes[0][2]],
      "R_v"))

for n, p in enumerate(paramsAOM[::2945]):
#    print("{:1.3e} \t{:1.3e} \t{:1.3e} \t{:1.3e}".format(
    print("{:} {:} {:} {:}".format(
            p[0], p[1], p[2], errors[n, 0]))
    
    


