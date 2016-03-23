# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 13:29:04 2016

@author: leportella
"""
import sys

sys.path.insert(0,'/home/leportella/scripts/pyscripts/myscripts/open')
import netCDF4 as nc
import matplotlib.pyplot as plt

a=nc.Dataset('/home/leportella/cluster/run/grd00/ocean_his_reg.nc')
zeta=a.variables['zeta'][:]
ubar=a.variables['ubar'][:]
vbar=a.variables['vbar'][:]
h=a.variables['h'][:]
maskr=a.variables['mask_rho'][:]

plt.figure()
plt.pcolor(zeta[-1,0,:,:])
plt.title('zeta')
plt.colorbar()

plt.figure()
plt.pcolor(ubar[-1,0,:,:])
plt.title('ubar')
plt.colorbar()

plt.figure()
plt.pcolor(vbar[-1,:,:])
plt.title('vbar')
plt.colorbar()

plt.figure()
plt.pcolor(h*maskr,vmin=0,vmax=3)
plt.title('h')
plt.colorbar()