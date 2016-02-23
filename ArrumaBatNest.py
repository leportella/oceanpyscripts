# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 21:42:21 2016

@author: leportella
"""

import sys

sys.path.insert(0,'/home/leportella/scripts/pyscripts/myscripts/open')
import netCDF4 as nc
from ncwork import *
import numpy as np
import matplotlib.pyplot as plt

grd1 = nc.Dataset('/home/leportella/Public/sclocal_scregv09_5x_batruim_roms.nc','r+')
grd2 = nc.Dataset('/home/leportella/Public/sclocal_scregv09_5x_batboa_roms.nc','r+')

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
#plt.pcolor(hfinal)

hfinal[hfinal<3]=3

grdfinal = nc.Dataset('/home/leportella/projects/runs/Run00/sclocal_scregv09_5x.nc','r+')
grdfinal['h'][:]=hfinal[:]
grdfinal['mask_rho'][:]=temp['mask_rho'][:]
grdfinal['mask_psi'][:]=temp['mask_psi'][:]
grdfinal['mask_u'][:]=temp['mask_u'][:]
grdfinal['mask_v'][:]=temp['mask_v'][:]




#grd2.variables['h'][:]=hfinal[:]