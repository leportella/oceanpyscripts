# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 19:32:46 2016

@author: leportella
"""


import sys

sys.path.insert(0,'/home/leportella/scripts/pyscripts/myscripts/open')

import netCDF4 as nc
import numpy as np
from ncwork import *
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pyproj import Proj

dirin = '/home/leportella/Documents/master/dados/vento/CFSR_datafiles/'


dado = nc.Dataset(dirin + 'wnd10m.cdas1.201104.grb2.nc')
var = GetVariables(dado)
var['lon']=np.subtract(var['lon'],360)

lat,lon = np.meshgrid(var['lat'],var['lon'], sparse=False, indexing='ij')

latmin=-27
latmax=-26
lonmin=-49
lonmax=-48

m = Basemap(projection='cyl', resolution='f', llcrnrlon=lonmin, llcrnrlat=latmin , urcrnrlon=lonmax , urcrnrlat=latmax )
fig = plt.figure()
m.drawcoastlines(linewidth=0.25,color = 'k')
m.fillcontinents(color='0.8',lake_color='aqua')
m.plot(lon,lat, 'r.', markersize=10,label=u'Disponível')
m.plot(var['lon'][12],var['lat'][3], 'b.', markersize=10,label='Selecionado')
plt.title(u'Pontos de Grade Modelo CFSR',fontsize=12)
#plt.legend([u'Disponível',u'Selecionado'],numpoints=1)
m.drawparallels(np.arange(latmin,latmax,0.5),labels=[1,0,0,0])
m.drawmeridians(np.arange(lonmin,lonmax,0.5),labels=[0,0,0,1])
#
