# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 13:29:04 2016

@author: leportella
"""

import sys

sys.path.insert(0,'/home/leportella/scripts/py/my/oceanpy/tools/')
import netCDF4 as nc
import matplotlib.pyplot as plt

a=nc.Dataset('/home/leportella/cluster/run/run17_run15_visc_mix_s/ocean_his_local_0007.nc')
zeta=a.variables['zeta'][-100:-1, :,:]
ubar=a.variables['ubar'][-100:-1, :,:]
vbar=a.variables['vbar'][-100:-1, :,:]
h=a.variables['h'][:]
maskr=a.variables['mask_rho'][:]

plt.figure()
plt.pcolor(zeta[:,:])
plt.title('zeta')
plt.colorbar()

plt.figure()
plt.pcolor(ubar[:,:])
plt.title('ubar')
plt.colorbar()

plt.figure()
plt.pcolor(vbar[:,:])
plt.title('vbar')
plt.colorbar()

plt.figure()
plt.pcolor(h*maskr,vmin=0,vmax=np.max(h))
plt.title('h')
plt.colorbar()