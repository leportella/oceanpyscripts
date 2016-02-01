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


grd1 = nc.Dataset('/home/leportella/projects/teste09/scregional_grd_v06_an.nc','r')
grd2 = nc.Dataset('/home/leportella/Public/scregional_grd_v06_an_v02_roms.nc','r')

h1 = grd1.variables['h'][:]
h2 = grd2.variables['h'][:]

h2[:,0]=h2[:,1]
h2[0,:]=h2[1,:]
h2[h2<=1]=1

h = np.zeros([202,277])

for i in range(len(h1)):
    for j in range(len(h1[0])):
        if i<=20:
            h[i,j] = i/20. * h2[i,j] + 1-(i/20.) * h1[i,j]
        elif i>20 and j<=20:
            h[i,j] = j/20. * h2[i,j] + 1-(j/20.) * h1[i,j]
        elif i>20 and j>=182:
             h[i,j] = (j-182)/20. * h1[i,j] + (202-j)/20. * h2[i,j]
        elif i>=257:
            h[i,j] = (i-257)/20. * h1[i,j] + (277-i)/20. * h2[i,j]
        else:
            h[i,j]= h2[i,j]

#h2
h = np.zeros([202,277])
for i in range(len(h1)):
    for j in range(len(h1[0])):
        if i<=10:
            h[i,j] = i/10.
        elif i>=192:
            h[i,j] = (202-i)/10.
        else:
            h[i,j]=1
            
for j in range(len(h1[0])):
    if j<=10:
        for i in range(j,len(h1)-j):
            h[i,j] = j/10.
    elif j>=267:
        ind = (277-j)
        print ind
        for i in range(ind,len(h1)-ind):
             h[i,j] = ind/10.
plt.pcolor(h)


hfinal = (h * h2) + ((1-h) * h1)