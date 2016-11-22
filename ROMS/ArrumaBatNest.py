# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 21:42:21 2016

@author: leportella
"""

import sys

sys.path.insert(0,'/home/leportella/scripts/py/my/oceanpy/tools')
import netCDF4 as nc
from ncwork import GetVariables, CreateMask
import numpy as np
import matplotlib.pyplot as plt

path = '/home/leportella/Public/regional2_v01/'
grd1 = nc.Dataset('{}local_reg2v01_5x_batruim.nc'.format(path),'r+')
grd2 = nc.Dataset('{}local_reg2v01_5x_batarrumada.nc'.format(path),'r+')

var = GetVariables(grd1)
var['h']=grd2.variables['h'][:]
temp = CreateMask(var)

h1 = grd1.variables['h'][:]
h2 = grd2.variables['h'][:]

h2[:,0]=h2[:,1]
h2[0,:]=h2[1,:]
#h2[h2<=1]=1

num = 20.
ti = len(h1)
tj = len(h1[0])


h = np.zeros([ti,tj])
for i in range(ti):
    for j in range(tj):
        if i<=num:
            h[i,j] = i/num
        elif i>=(ti-num):
            h[i,j] = (ti-i)/num
        else:
            h[i,j]=1
            
for j in range(tj):
    if j<=num:
        for i in range(j,ti-j):
            h[i,j] = j/num
    elif j>=(tj-num):
        ind = (tj-j)
        print ind
        for i in range(ind,ti-ind):
             h[i,j] = ind/num

hfinal = (h * h2) + ((1-h) * h1)
plt.pcolor(hfinal)

hfinal[hfinal<3]=3

outpath = '/home/leportella/projects/files/regional2_v01/'
grdfinal = nc.Dataset('local_reg2v01_5x.nc','r+')
grdfinal.variables['h'][:]=hfinal[:]

#grdfinal.variables['mask_rho'][:]=temp['mask_rho'][:]
#grdfinal.variables['mask_psi'][:]=temp['mask_psi'][:]
#grdfinal.variables['mask_u'][:]=temp['mask_u'][:]
#grdfinal.variables['mask_v'][:]=temp['mask_v'][:]

#grdfinal.variables['x_rho'][:]=grd1.variables['x_rho'][:]
#grdfinal.variables['y_rho'][:]=grd1.variables['y_rho'][:]
#grdfinal.variables['x_psi'][:]=grd1.variables['x_psi'][:]
#grdfinal.variables['y_psi'][:]=grd1.variables['y_psi'][:]
#grdfinal.variables['x_u'][:]=grd1.variables['x_u'][:]
#grdfinal.variables['y_u'][:]=grd1.variables['y_u'][:]
#grdfinal.variables['x_v'][:]=grd1.variables['x_v'][:]
#grdfinal.variables['y_v'][:]=grd1.variables['y_v'][:]

#grd2.variables['h'][:]=hfinal[:]