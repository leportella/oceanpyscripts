# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 17:00:14 2016

@author: leportella
"""

import netCDF4 as nc
import numpy as np

g = nc.Dataset('/home/leportella/projects/cdl/bry_unlimit.nc','r+')

xsi_rho = 398
eta_rho = 499

for var in g.variables:
    print(var)

g.variables['zeta_west'][:] = np.zeros((2, eta_rho))
g.variables['zeta_east'][:] =  np.zeros((2, eta_rho))
g.variables['zeta_south'][:] = np.zeros((2, xsi_rho))
g.variables['zeta_north'][:] = np.zeros((2, xsi_rho))

g.variables['ubar_north'][:] = np.multiply(0, g.variables['ubar_north'][:])
g.variables['ubar_south'][:] = np.multiply(0, g.variables['ubar_south'][:])
g.variables['ubar_west'][:] = np.multiply(0, g.variables['ubar_west'][:])
g.variables['ubar_east'][:] =  np.multiply(0, g.variables['ubar_east'][:])

g.variables['vbar_north'][:] = np.multiply(0, g.variables['vbar_north'][:])
g.variables['vbar_south'][:] = np.multiply(0, g.variables['vbar_south'][:])
g.variables['vbar_west'][:] = np.multiply(0, g.variables['vbar_west'][:])
g.variables['vbar_east'][:] = np.multiply(0, g.variables['vbar_east'][:])

g.variables['bry_time'][:] = np.array([0, 100000])



example = nc.Dataset('/home/leportella/projects/runs/run07_igual01a_vento/bry_unlimit.nc')
ee = {}
for var in example.variables:
    ee[var] = example.variables[var][:]
bry = example.variables['bry_time'][:]