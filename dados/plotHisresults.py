# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 23:30:12 2016

@author: leportella
"""

import sys

sys.path.insert(0, '/home/leportella/scripts/py/my/oceanpy/tools/')

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import netCDF4 as nc
import numpy as np

run = 'Run01a'
basedir = '/home/leportella/Documents/master/dissertacao/Latex/dis_controlada'
dirOut = basedir + '/figuras/{}/'.format(run)


###############################################################################
##                                                                           ##
##                           GRADE REGIONAL                                  ##
##                                                                           ##
###############################################################################

clusterdir = '/home/leportella/cluster/run'
passo = 100
regional = nc.Dataset(clusterdir + '/{}/ocean_his_reg.nc'.format(run))
lon = regional.variables['lon_rho'][:]
lat = regional.variables['lat_rho'][:]
print 'Lat lon lidas'
zeta = regional.variables['zeta'][0:passo,:,:]
print 'Zeta lido'
otime = regional.variables['ocean_time'][0:passo]
print 'Modelo lido'

initdate=datetime(2011,1,1,0,0,0)
tempo = []
for t in otime:
    tempo.append(np.add(initdate, timedelta(seconds=int(t))))
print 'Tempo ok!'

latmin=-28.2
latmax=-25.4
lonmin=-49.2
lonmax=-47
m = Basemap(projection='cyl',
            resolution='f',
            llcrnrlon=lonmin,
            llcrnrlat=latmin,
            urcrnrlon=lonmax,
            urcrnrlat=latmax,
           )
print 'Basemap ok!'

for i in range(0,len(zeta)):
    fig = plt.figure()
    im1 = m.pcolormesh(lon,
                       lat,
                       zeta[i,:,:],
                       shading='flat',
                       cmap=plt.cm.viridis,
                       latlon=True,
                       vmin=-0.2,
                       vmax=0.2
                      )
    m.drawcoastlines(linewidth=0.25, color = 'k')
    m.fillcontinents(color='0.8', lake_color='aqua')
    m.drawparallels(np.arange(latmin, latmax,1), labels=[1,0,0,0])
    m.drawmeridians(np.arange(lonmin, lonmax,1), labels=[0,0,0,1])
    cb = m.colorbar(im1, "right", size="5%", pad="2%")
    plt.title('Tempo: '+ str(tempo[i]))
    plt.savefig(dirOut + 'Run01a_TS_' + str(i) +'.png', dpi=200)
    print 'Tempo ' + str(i) + ' ok!'
