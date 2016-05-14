#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 11:23:20 2015

@author: leportella
"""
import sys

sys.path.insert(0,'/home/leportella/scripts/pyscripts/myscripts/open')
import netCDF4 as nc
from ncwork import *
from pyproj import Proj
import romslab as rl

# NÃO ESQUECER: BATIMETRIA POSIvTIVA PRA BAIXO!


###############################################################################
##                                                                           ##
##                      CRIANDO GRID (BASE: RGFGRID)                         ##
##                                                                           ##
###############################################################################
init=nc.Dataset('/home/leportella/Public/scregional_grdv10_delftversion_roms.nc')


###### Primeira etapa ############
out = rgfgrid2ROMS(init)

###### Convert Coordinates #######
myProj = Proj("+proj=utm +zone=22J, +south +ellps=WGS84 +datumWS84 +units=m +no_defs")

lon,lat = UTM2geo(out['x_rho'][:],out['y_rho'][:],myProj)
out['lon_rho']=lon[:]
out['lat_rho']=lat[:]

lonp,latp = UTM2geo(out['x_psi'][:],out['y_psi'][:],myProj)
out['lon_psi']=lonp[:]
out['lat_psi']=latp[:]

lonu,latu = UTM2geo(out['x_u'][:],out['y_u'][:],myProj)
out['lon_u']=lonu[:]
out['lat_u']=latu[:]

lonv,latv = UTM2geo(out['x_v'][:],out['y_v'][:],myProj)
out['lon_v']=lonv[:]
out['lat_v']=latv[:]

###### Angle and Coriolis #######
out['pm'],out['pn'],out['dndx'],out['dmde']=rl.get_metrics(out['lat_u'],out['lon_u'],out['lat_v'],out['lon_v'])
out['f']= CalculateCoriolis(out['lat_rho'])

###### Creating Mask #######
temp = CreateMask(out)
out['mask_rho']=temp['mask_rho']
out['mask_psi']=temp['mask_psi']
out['mask_u']=temp['mask_u']
out['mask_v']=temp['mask_v']

out['h'][out['h']<3]=3

###### Inserting data on NC #######

grd = nc.Dataset('/home/leportella/projects/runs/Run00/scregional_grdv10.nc','r+')
InsertGridDimensions(grd,out)
grd.close()


import matplotlib.pyplot as plt
plt.pcolor(out['mask_rho'])
plt.colorbar()

######################## GRADE ANINHADA ##########################
#grd2 = nc.Dataset('/home/leportella/projects/teste09/scregional_grd_v06_an.nc','r+')
#myProj = Proj("+proj=utm +zone=22J, +south +ellps=WGS84 +datumWS84 +units=m +no_defs")
#
## lon e lat de rho
#lon = grd2.variables['lon_rho'][:]
#lat = grd2.variables['lat_rho'][:]
#
#x,y = geo2UTM(lat,lon,myProj)
#
#grd2.variables['x_rho'][:]=x[:]
#grd2.variables['y_rho'][:]=y[:]
#
### lon e lat de psi
#lonp = grd2.variables['lon_psi'][:]
#latp = grd2.variables['lat_psi'][:]
#
#xp,yp = geo2UTM(latp,lonp,myProj)
#
#grd2.variables['x_psi'][:]=xp[:]
#grd2.variables['y_psi'][:]=yp[:]
#
### lon e lat de u
#lonu = grd2.variables['lon_u'][:]
#latu = grd2.variables['lat_u'][:]
#
#xu,yu = geo2UTM(latu,lonu,myProj)
#
#grd2.variables['x_u'][:]=xu[:]
#grd2.variables['y_u'][:]=yu[:]
#
### lon e lat de v
#lonv = grd2.variables['lon_v'][:]
#latv = grd2.variables['lat_v'][:]
#
#xv,yv = geo2UTM(latv,lonv,myProj)
#
#grd2.variables['x_v'][:]=xv[:]
#grd2.variables['y_v'][:]=yv[:]
#
#grd2.close()
#
#
#
#
#import shutil
#shutil.copy2('/home/leportella/projects/teste01/grd_spherical.nc', '/home/leportella/projects/teste01/grd_spherical_backup.nc')