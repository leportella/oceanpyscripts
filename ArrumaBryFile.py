# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 11:43:24 2016

@author: leportella
"""
import numpy as np
import netCDF4 as nc

a = nc.Dataset('/home/leportella/projects/cdl/bry_unlimit.nc','r+')

xsi_rho = 598
xsi_u = 597
xsi_v = 598
eta_rho = 1098
eta_u = 1098
eta_v = 1097
time = 2

a.variables['bry_time'][:]=np.array([0,9229371983])[:]

a.variables['zeta_east'][:]= np.zeros([time,eta_rho])[:]
a.variables['zeta_west'][:]= np.zeros([time,eta_rho])[:]
a.variables['zeta_north'][:]= np.zeros([time,xsi_rho])[:]
a.variables['zeta_south'][:]= np.zeros([time,xsi_rho])[:]

a.variables['ubar_east'][:]= np.zeros([time,eta_u])[:]
a.variables['ubar_west'][:]= np.zeros([time,eta_u])[:]
a.variables['ubar_north'][:]= np.zeros([time,xsi_u])[:]
a.variables['ubar_south'][:]= np.zeros([time,xsi_u])[:]

a.variables['vbar_east'][:]= np.zeros([time,eta_v])[:]
a.variables['vbar_west'][:]= np.zeros([time,eta_v])[:]
a.variables['vbar_north'][:]= np.zeros([time,xsi_v])[:]
a.variables['vbar_south'][:]= np.zeros([time,xsi_v])[:]

a.close()