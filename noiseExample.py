# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 01:43:05 2018

@author: Adrian
"""

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel

import numpy as np
import matplotlib.pyplot as pl
pl.style.use(r"prl.mplstyle")

N = 21
exess = 0.3
f = lambda x: np.sin(x)

x = np.linspace(-exess, 2*np.pi + exess, 1000)
y = f(x)

obsX = np.linspace(0, 2*np.pi, N)
noise = (np.random.random(obsX.shape) - 0.5)
obsY = f(obsX + noise)


# No optimization
def optimizer(obj_func, initial_theta, bounds):
    return initial_theta, 0

# hyperparameter fit example
kernel1 = RBF()
model1 = GaussianProcessRegressor(kernel = kernel1, 
                                  optimizer = 'fmin_l_bfgs_b',
                                  n_restarts_optimizer = 20)
model1.fit(obsX.reshape(-1, 1),
          obsY.reshape(-1, 1))
ax1 = pl.subplot(211)
#pl.grid()
pl.plot(x, y, label = 'Source')
_preY, errY = model1.predict(x.reshape(-1, 1), return_std = True)
preY = _preY.T[0]
pl.fill_between(x, preY - errY, preY + errY, color = '0.5', alpha = 0.3, label = 'Error')
pl.plot(x, preY, label = 'Prediction')
pl.plot(obsX, obsY, '^k', label = 'Observation', ms = 5.)

pl.ylabel('Unfit', fontsize=12.)
pl.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=43, mode="expand", borderaxespad=0., fontsize=10.)

pl.subplot(212, sharex=ax1)

kernel2 = RBF() + WhiteKernel()
model2 = GaussianProcessRegressor(kernel = kernel2, 
                                  optimizer = 'fmin_l_bfgs_b',
                                  n_restarts_optimizer = 20)
model2.fit(obsX.reshape(-1, 1),
          obsY.reshape(-1, 1))
pl.plot(x, y)
_preY, errY = model2.predict(x.reshape(-1, 1), return_std = True)
preY = _preY.T[0]
pl.fill_between(x, preY - errY, preY + errY, color = '0.5', alpha = 0.3)
pl.plot(x, preY)
pl.plot(obsX, obsY, '^k', ms = 5.)
pl.ylabel('Fit', fontsize=12.)



pl.xlim(min(x), max(x))
pl.savefig('WhiteKernelFit.pdf', format='pdf', dpi=1000)
pl.show()
