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
import numpy as np


# NÃO ESQUECER: BATIMETRIA POSIvTIVA PRA BAIXO!


###############################################################################
##                                                                           ##
##                      CRIANDO GRID (BASE: RGFGRID)                         ##
##                                                                           ##
###############################################################################
init=nc.Dataset('/home/leportella/Public/batnova_grd07.nc')

out = rgfgrid2ROMS(init)

grd = nc.Dataset('/home/leportella/projects/teste09/scregional_grd_v07_sm.nc','r+')

InsertGridDimensions(grd,out)

grd.close()

grd = nc.Dataset('/home/leportella/projects/teste09/scregional_grd_v08_sm.nc','r+')
h=grd.variables['h'][:]
h[h<=3]=3.
grd.variables['h'][:]=h[:]
grd.close()
###############################################################################
##                                                                           ##
##                      CONVERT COORDINATES                                  ##
##                                                                           ##
###############################################################################


myProj = Proj("+proj=utm +zone=22J, +south +ellps=WGS84 +datumWS84 +units=m +no_defs")
grd = nc.Dataset('/home/leportella/projects/teste09/scregional_grd_v07_sm.nc','r+')

lon = grd.variables['lon_rho'][:]
lat = grd.variables['lat_rho'][:]

x,y = geo2UTM(lat,lon,myProj)

grd.variables['x_rho'][:]=x[:]
grd.variables['y_rho'][:]=y[:]


## lon e lat de psi
lonp = grd.variables['lon_psi'][:]
latp = grd.variables['lat_psi'][:]

xp,yp = geo2UTM(latp,lonp,myProj)

grd.variables['x_psi'][:]=xp[:]
grd.variables['y_psi'][:]=yp[:]

## lon e lat de u
lonu = grd.variables['lon_u'][:]
latu = grd.variables['lat_u'][:]

xu,yu = geo2UTM(latu,lonu,myProj)

grd.variables['x_u'][:]=xu[:]
grd.variables['y_u'][:]=yu[:]

## lon e lat de v
lonv = grd.variables['lon_v'][:]
latv = grd.variables['lat_v'][:]

xv,yv = geo2UTM(latv,lonv,myProj)

grd.variables['x_v'][:]=xv[:]
grd.variables['y_v'][:]=yv[:]

grd.close()


####################### GRADE ANINHADA ##########################
grd2 = nc.Dataset('/home/leportella/projects/teste09/scregional_grd_v06_an.nc','r+')
myProj = Proj("+proj=utm +zone=22J, +south +ellps=WGS84 +datumWS84 +units=m +no_defs")

# lon e lat de rho
lon = grd2.variables['lon_rho'][:]
lat = grd2.variables['lat_rho'][:]

x,y = geo2UTM(lat,lon,myProj)

grd2.variables['x_rho'][:]=x[:]
grd2.variables['y_rho'][:]=y[:]

## lon e lat de psi
lonp = grd2.variables['lon_psi'][:]
latp = grd2.variables['lat_psi'][:]

xp,yp = geo2UTM(latp,lonp,myProj)

grd2.variables['x_psi'][:]=xp[:]
grd2.variables['y_psi'][:]=yp[:]

## lon e lat de u
lonu = grd2.variables['lon_u'][:]
latu = grd2.variables['lat_u'][:]

xu,yu = geo2UTM(latu,lonu,myProj)

grd2.variables['x_u'][:]=xu[:]
grd2.variables['y_u'][:]=yu[:]

## lon e lat de v
lonv = grd2.variables['lon_v'][:]
latv = grd2.variables['lat_v'][:]

xv,yv = geo2UTM(latv,lonv,myProj)

grd2.variables['x_v'][:]=xv[:]
grd2.variables['y_v'][:]=yv[:]

grd2.close()




import shutil
shutil.copy2('/home/leportella/projects/teste01/grd_spherical.nc', '/home/leportella/projects/teste01/grd_spherical_backup.nc')