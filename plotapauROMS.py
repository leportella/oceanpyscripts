# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 13:29:04 2016

@author: leportella
"""
import sys

sys.path.insert(0,'/home/leportella/scripts/pyscripts/myscripts/open')
import netCDF4 as nc
from ncwork import *
import matplotlib.pyplot as plt

a=nc.Dataset('/home/leportella/projects/teste09/ocean_rst_reg.nc')

var = GetVariables(a)


plt.figure()
plt.pcolor(var['zeta'][-1,:,:])
plt.title('zeta')
plt.colorbar()

plt.figure()
plt.pcolor(var['ubar'][-1,:,:])
plt.title('ubar')
plt.colorbar()

plt.figure()
plt.pcolor(var['vbar'][-1,:,:])
plt.title('vbar')
plt.colorbar()

plt.figure()
plt.pcolor(var['h'][:]*var['mask_rho'][:],vmin=0,vmax=3)
plt.title('h')
plt.colorbar()