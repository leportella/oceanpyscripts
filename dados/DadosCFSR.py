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
from generaltools import *
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pyproj import Proj
import datetime
from windrose import WindroseAxes

dirin='/home/leportella/Documents/master/dados/vento/CFSR_datafiles/files/'
dirOut = '/home/leportella/Documents/master/dissertacao/Latex/dis_controlada/figuras/'

anos = range(2011,2016)
meses = range(1,13)


c=1

u=[]
v=[]
tempo=[]
uv = [[],[]]

for ano in anos:
    for mes in meses:
        f = dirin + 'wnd10m.dd.%04d%02d.grb2.nc' % (ano, mes)
        dado = nc.Dataset(f)
        var = GetVariables(dado)
        
        if c==1:
            lon1=var['lon']-360
            lat1=var['lat']
        
        for t in range(len(var['time'])):
            u.append(var['U_GRD_L103'][t,:,:])
            v.append(var['V_GRD_L103'][t,:,:])
            uv[0].append(u[t][3,12])
            uv[1].append(v[t][3,12])
            tano = var['valid_date_time'][t][0]+var['valid_date_time'][t][1]+var['valid_date_time'][t][2]+                var['valid_date_time'][t][3]
            tmes = var['valid_date_time'][t][4]+var['valid_date_time'][t][5]
            tdia = var['valid_date_time'][t][6]+var['valid_date_time'][t][7]
            thora =var['valid_date_time'][t][8]+var['valid_date_time'][t][9]
            tempo.append(datetime.datetime(
                    int(tano), int(tmes), int(tdia), int(thora), 0, 0))
        c=+1
                
            
cfsr = uv2veldir_wind(uv[0],uv[1])
cfsr['tempo']=tempo

#################### WINDROSE ################################
plotaWindRose(cfsr['dir'],cfsr['vel'],maxYlabel=20, maxLeg=9, stepLeg=2)  
plt.savefig(dirOut + 'Vento_CFSR_2011-15_Windrose.png',dpi=200)

################### PLOT VEL ################################
plt.figure(figsize=(15,5))
plt.plot(tempo[0:8758],cfsr['vel'][0:8758])
plt.title(u'Velocidade do Vento - CFSR')
plt.ylabel(u'Velocidade (m/s)')
plt.grid()
plt.savefig(dirOut + 'Vento_CFSR_2011-15_vel.png',dpi=200)

################# HISTOGRAMA VEL VENTO  ###################
PercentHistogram(cfsr['vel'],binss=50)
plt.title(u'Histograma de Velocidade do Vento - CFSR')
plt.ylabel(u'Percentual')
plt.xlabel(u'Velocidade (m/s)')
plt.xlim(0,10)
plt.grid()
plt.savefig(dirOut + 'Vento_CFSR_2011_histvel.png',dpi=200)

################# HISTOGRAMA DIR VENTO  ###################
PercentHistogram(cfsr['dir'],binss=50)
plt.title(u'Histograma de Direção do Vento - CFSR')
plt.ylabel(u'Percentual')
plt.xlabel(u'Velocidade (m/s)')
plt.xlim(0,360)
plt.grid()
plt.savefig(dirOut + 'Vento_CFSR_2011_histdir.png',dpi=200)


#lat,lon = np.meshgrid(lat1,lon1, sparse=False, indexing='ij')
#
#latmin=-27.2
#latmax=-26.2
#lonmin=-49
#lonmax=-48
#
#m = Basemap(projection='cyl', resolution='f', llcrnrlon=lonmin, llcrnrlat=latmin , urcrnrlon=lonmax , urcrnrlat=latmax )
#fig = plt.figure()
#m.drawcoastlines(linewidth=0.25,color = 'k')
#m.fillcontinents(color='0.8',lake_color='aqua')
##m.plot(lon,lat, 'r.', markersize=10,label=u'Disponível')
#m.plot(lon1[12],lat1[3], 'r.', markersize=10,label='CFSR')
#m.plot(-48.651,-26.8833, 'b.', markersize=10,label='METAR') #aeroporto navegantes
#plt.title(u'Dados de Vento Analisados',fontsize=12)
#plt.legend([u'CFSR',u'METAR'],numpoints=1)
#m.drawparallels(np.arange(latmin,latmax,0.5),labels=[1,0,0,0])
#m.drawmeridians(np.arange(lonmin,lonmax,0.5),labels=[0,0,0,1])
#plt.savefig(dirOut + 'DadosVento_position.png',dpi=200)
#
