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

grd1 = nc.Dataset('/home/leportella/projects/teste09/sclocal_screg07_5x_batruim.nc','r')
grd2 = nc.Dataset('/home/leportella/projects/teste09/sclocal_screg07_5x.nc','r+')

h1 = grd1.variables['h'][:]
h2 = grd2.variables['h'][:]

h2[:,0]=h2[:,1]
h2[0,:]=h2[1,:]
h2[h2<=1]=1

#h = np.zeros([202,277])
#
#for i in range(len(h1)):
#    for j in range(len(h1[0])):
#        if i<=20:
#            h[i,j] = i/20. * h2[i,j] + 1-(i/20.) * h1[i,j]
#        elif i>20 and j<=20:
#            h[i,j] = j/20. * h2[i,j] + 1-(j/20.) * h1[i,j]
#        elif i>20 and j>=182:
#             h[i,j] = (j-182)/20. * h1[i,j] + (202-j)/20. * h2[i,j]
#        elif i>=257:
#            h[i,j] = (i-257)/20. * h1[i,j] + (277-i)/20. * h2[i,j]
#        else:
#            h[i,j]= h2[i,j]

#h2
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

grd2.variables['h'][:]=hfinal[:]