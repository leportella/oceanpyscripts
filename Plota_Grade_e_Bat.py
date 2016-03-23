# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 10:05:38 2016

@author: leportella
"""

import sys

sys.path.insert(0,'/home/leportella/scripts/pyscripts/myscripts/open')

import netCDF4 as nc
import numpy as np
from generaltools import *
from ncwork import *
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pyproj import Proj

direct = '/home/leportella/Documents/master/dados/utilizacao/'
dirOut = '/home/leportella/Documents/master/dissertacao/Latex/dis_controlada/figuras/'

myProj = Proj("+proj=utm +zone=22J, +south +ellps=WGS84 +datumWS84 +units=m +no_defs")



#################################################################################
##                                                                             ##
##                             GRADE REGIONAL                                  ##
##                                                                             ##
#################################################################################    

r = nc.Dataset('/home/leportella/projects/runs/Run00/scregional_grdv10.nc','r+')
var=GetVariables(r)

latmin=-28.2
latmax=-25.4
lonmin=-49.2
lonmax=-47
m = Basemap(projection='cyl', resolution='f', llcrnrlon=lonmin, llcrnrlat=latmin , urcrnrlon=lonmax , urcrnrlat=latmax )

fig = plt.figure()
m.drawcoastlines(linewidth=0.25,color = 'k')
m.fillcontinents(color='0.8',lake_color='aqua')
m.plot(var['lon_rho'],var['lat_rho'], 'r.', markersize=.05,label='Ponto Medido')
plt.title(u'Domínio da Grade Numérica Regional',fontsize=12)
m.drawparallels(np.arange(latmin,latmax,1),labels=[1,0,0,0])
m.drawmeridians(np.arange(lonmin,lonmax,1),labels=[0,0,0,1])
plt.savefig(dirOut + 'GradeRegional.png',dpi=200)

fig = plt.figure()
m.drawcoastlines(linewidth=0.25,color = 'k')
m.fillcontinents(color='0.8',lake_color='aqua')
m.pcolormesh(var['lon_rho'],var['lat_rho'],var['h'],shading='flat',cmap=plt.cm.viridis,latlon=True,vmin=0,vmax=150)
plt.colorbar(fraction=0.046 )
plt.title(u'Batimetria da Grade Numérica Regional',fontsize=12)
m.drawparallels(np.arange(latmin,latmax,1),labels=[1,0,0,0])
m.drawmeridians(np.arange(lonmin,lonmax,1),labels=[0,0,0,1])
plt.savefig(dirOut + 'Batimetria_GrdRegional.png',dpi=200)



#################################################################################
##                                                                             ##
##                                GRADE LOCAL                                  ##
##                                                                             ##
#################################################################################    

r = nc.Dataset('/home/leportella/projects/runs/Run00/sclocal_scregv10_5x.nc','r+')
var=GetVariables(r)
lonr,latr = UTM2geo(r.variables['x_rho'][:],r.variables['y_rho'][:],myProj)

latmin=-26.88
latmax=-26.45
lonmin=-48.8
lonmax=-48.2

m = Basemap(projection='cyl', resolution='f', llcrnrlon=lonmin, llcrnrlat=latmin , urcrnrlon=lonmax , urcrnrlat=latmax )

fig = plt.figure()
m.drawcoastlines(linewidth=0.25,color = 'k')
m.fillcontinents(color='0.8',lake_color='aqua')
m.plot(lonr,latr, 'r.', markersize=.05,label='Ponto Medido')
plt.title(u'Domínio da Grade Numérica Local',fontsize=12)
m.drawparallels(np.arange(latmin,latmax,0.2),labels=[1,0,0,0])
m.drawmeridians(np.arange(lonmin,lonmax,0.2),labels=[0,0,0,1])
plt.savefig(dirOut + 'GradeLocal.png',dpi=200)


fig = plt.figure()
m.drawcoastlines(linewidth=0.25,color = 'k')
m.fillcontinents(color='0.8',lake_color='aqua')
m.pcolormesh(lonr,latr,var['h'],shading='flat',cmap=plt.cm.viridis,latlon=True,vmin=0,vmax=45)
plt.colorbar(shrink=.78)
plt.title(u'Batimetria da Grade Numérica Local',fontsize=12)
m.drawparallels(np.arange(latmin,latmax,0.2),labels=[1,0,0,0])
m.drawmeridians(np.arange(lonmin,lonmax,0.2),labels=[0,0,0,1])
plt.savefig(dirOut + 'Batimetria_GrdRLocal.png',dpi=200)

