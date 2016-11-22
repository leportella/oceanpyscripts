# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 22:26:38 2016

@author: leportella
"""

import sys

sys.path.insert(0, '/home/leportella/scripts/py/my/oceanpy/tools')

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from estatisticatools import calcula_ema, calcula_remq, calcula_ia
from generaltools import *
from mpl_toolkits.basemap import Basemap
from ncwork import *

direct = '/home/leportella/Documents/master/dados/utilizacao/'
dirOut = ('/home/leportella/Documents/master/dissertacao/Latex/'
          'dis_controlada/figuras')

############################### Dados Modelados #################################

run = 'run10_regional2_mare'
num_files = 2

local = ReadROMSResults(run, 'local', num_files, uv=False)
#reg = ReadROMSResults(run, 'reg', num_files, uv=False)


# Arrumando o tempo de referencia pra tempo real e tempo local
refdate = '20110101'
timevector = local['reftime']
local['time'] = FindTimeVector(refdate, timevector)

latmin=-26.85
latmax=-26.55
lonmin=-48.70
lonmax=-48.22

m = Basemap(projection='cyl',
            resolution='f',
            llcrnrlon=lonmin,
            llcrnrlat=latmin,
            urcrnrlon=lonmax,
            urcrnrlat=latmax,
           )
print 'Basemap ok!'

for i in range(0,len(local['time'])):
    fig = plt.figure()
    im1 = m.pcolormesh(local['lonr'],
                       local['latr'],
                       local['zeta'][i,:,:],
                       shading='flat',
                       cmap=plt.cm.viridis,
                       latlon=True,
                       vmin=-0.4,
                       vmax=0.4
                      )
    m.drawcoastlines(linewidth=0.25, color = 'k')
    m.fillcontinents(color='0.8', lake_color='aqua')
    m.drawparallels(np.arange(latmin, latmax+0.1, 0.1), labels=[1,0,0,0])
    m.drawmeridians(np.arange(lonmin, lonmax, 0.2), labels=[0,0,0,1])
    cb = m.colorbar(im1, "right", size="5%", pad="2%")
    plt.title('Tempo: '+ str(local['time'][i]))
    plt.savefig('{}/{}/TS_{}.png'.format(dirOut, run, i), dpi=200)
    print 'Tempo ' + str(i) + ' ok!'




