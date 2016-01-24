# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 23:30:12 2016

@author: leportella
"""

import sys

sys.path.insert(0,'/home/leportella/scripts/pyscripts/myscripts/open')

import netCDF4 as nc
import numpy as np
from ncwork import *
import romslab as rl
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

dirOut = '/home/leportella/projects/teste06/results/'

#class ReadROMSHisfile(object):
#    """Load the output roms history """
#    def __init__(self, filename):
#        self.ncfile = nc.Dataset(filename)
#        self.varlist = list(self.ncfile.variables)
##        self.temp = self.ncfile.variables['temp']
#        self.lon_rho = self.ncfile.variables['lon_rho']
#        self.lat_rho = self.ncfile.variables['lat_rho']
#        self.lon_u = self.ncfile.variables['lon_u']
#        self.lat_u = self.ncfile.variables['lat_u']
#        self.lon_v = self.ncfile.variables['lon_v']
#        self.lat_v = self.ncfile.variables['lat_v']
#        self.zeta = self.ncfile.variables['zeta']
#        self.u = self.ncfile.variables['ubar_eastward'][:,-1,...]
#        self.v = self.ncfile.variables['vbar_northward'][:,-1,...]
#        self.ang = self.ncfile.variables['angle']


teste = nc.Dataset('/home/leportella/projects/teste06/ocean_his.nc')
lon=teste.variables['lon_rho'][:]
lat=teste.variables['lat_rho'][:]
zeta=teste.variables['zeta'][:]


m = Basemap(projection='cyl', resolution='f', llcrnrlon= -49.3, llcrnrlat= -29.2, urcrnrlon= -47, urcrnrlat= -26)
 
for i in range(0,len(zeta)):
    fig = plt.figure()
    im1 = m.pcolormesh(lon,lat,zeta[i,:,:],shading='flat',cmap=plt.cm.viridis,latlon=True,vmin=-0.2,vmax=0.2)
    m.drawcoastlines(linewidth=0.25,color = 'k')
    m.fillcontinents(color='0.8',lake_color='aqua')
    cb = m.colorbar(im1,"right", size="5%", pad="2%")
    plt.title('Tempo: '+ str(i))
    plt.savefig(dirOut + 'Teste06_TS_' + str(i) +'.png',dpi=200)
    print 'Tempo ' + str(i) + ' ok!'

