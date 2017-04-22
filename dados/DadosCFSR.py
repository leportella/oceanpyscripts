# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 19:32:46 2016

@author: leportella
"""


import sys

sys.path.insert(0,'/home/leportella/scripts/py/my/oceanpy/tools')

import netCDF4 as nc
import numpy as np
from ncwork import GetVariables
from generaltools import uv2veldir_wind
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pyproj import Proj
import datetime

# dirin='/home/leportella/Documents/master/dados/vento/CFSR_WindStress/wind_stress'
dirin='/home/leportella/Documents/master/dados/vento/CFSR_UV_1h'
dirOut = '/home/leportella/Documents/master/dissertacao/Latex/dis_controlada/figuras/vento/'

anos = range(2011, 2016)
#anos=[2011]
meses = range(1,13); epoca = r'Total'
#meses=[12, 1, 2]; epoca = r'Verao'
#meses=[3, 4, 5]; epoca = u'Outono'
#meses=[6, 7, 8]; epoca = u'Inverno'
#meses=[9, 10, 11]; epoca = u'Primavera'


c=1

u=[]
v=[]
tempo=[]
tempo_minutos=[]
uv = [[],[]]
time = []

for ano in anos:
    for mes in meses:
        # f = dirin + '/wndstrs.cdas1.%04d%02d.grb2.nc' % (ano, mes)
        f = dirin + '/wnd10m.cdas1.%04d%02d.grb2.nc' % (ano, mes)
        dado = nc.Dataset(f)
        var = GetVariables(dado)
        
        print ano
        print mes
        
        if c==1:
            lon1=var['lon']-360
            lat1=var['lat'][::-1]
        
        for t in range(len(var['time'])):
#            u_cfsr = var['U_FLX_L1_Avg_1'][t,:,:]
#            v_cfsr = var['V_FLX_L1_Avg_1'][t,:,:]
            u_cfsr = var['V_GRD_L103'][t,:,:]
            v_cfsr = var['U_GRD_L103'][t,:,:]
        

            u.append(u_cfsr[::-1,:])
            v.append(v_cfsr[::-1,:])
            
            uv[0].append(u[t][11,13])
            uv[1].append(v[t][11,13])
            
            tt = var['ref_date_time'][:]
            tano = tt[t][0]+tt[t][1]+tt[t][2]+tt[t][3]
            tmes = tt[t][4]+tt[t][5]
            tdia = tt[t][6]+tt[t][7]
            thora = tt[t][8]+tt[t][9]
            temp = np.subtract(datetime.datetime(
                    int(tano), int(tmes), int(tdia), int(thora), 0, 0), 
                    datetime.datetime(2011,1,1,0,0,0))
            tempo.append(temp.total_seconds())
            tempo_minutos.append(temp.total_seconds()/60.)
            time.append(datetime.datetime(
                int(tano), int(tmes), int(tdia), int(thora), 0, 0))
        c=+1
        dado.close()
                

            
cfsr = uv2veldir_wind(uv[0],uv[1])
cfsr['tempo']=tempo
cfsr['time'] = time

###################### GERA NETCDF DE FORCANTE ################################
#a = nc.Dataset('/home/leportella/projects/cdl/frc_bulk_windstrs_latinvertido.nc','r+')
#a.variables['lon'][:]= np.array(lon1)
#a.variables['lat'][:]= np.array(lat1)
#a.variables['time'][:]= np.array(tempo)
#a.variables['sustr'][:]= np.array(u)
#a.variables['svstr'][:]= np.array(v)
#a.close()

##################### WINDROSE ################################
plotaWindRose(cfsr['dir'],cfsr['vel'],maxYlabel=20, maxLeg=14, stepLeg=2)  
plt.savefig(dirOut + 'Vento_CFSR_2011-15_Windrose_{}.png'.format(epoca), dpi=200)
#
#################### PLOT VEL ################################
plt.figure(figsize=(15,5))
plt.plot(time, cfsr['vel'])
plt.title(u'Velocidade do Vento - {} - CFSR'.format(epoca))
plt.ylabel(u'Velocidade (m/s)')
plt.xlim(time[0], time[-1])
plt.grid()
plt.savefig(dirOut + 'Vento_CFSR_2011-15_vel_{}.png'.format(epoca), dpi=200)
#

############## HISTOGRAMA VEL VENTO  ###################
PercentHistogram(cfsr['vel'],binss=50)
plt.title(u'Histograma de Velocidade do Vento - {} - CFSR'.format(epoca))
plt.ylabel(u'Percentual')
plt.xlabel(u'Velocidade (m/s)')
plt.xlim(0,10)
plt.grid()
plt.savefig(dirOut + 'Vento_CFSR_2011-15_histvel_{}.png'.format(epoca), dpi=200)

################## HISTOGRAMA DIR VENTO  ###################
PercentHistogram(cfsr['dir'],binss=50)
plt.title(u'Histograma de Direção do Vento - {} - CFSR'.format(epoca))
plt.ylabel(u'Percentual')
plt.xlabel(u'Direção em Graus')
plt.xlim(0,360)
plt.grid()
plt.savefig(dirOut + 'Vento_CFSR_2011-15_histdir_{}.png'.format(epoca), dpi=200)
#
#
lat,lon = np.meshgrid(lat1,lon1, sparse=False, indexing='ij')

latmin=-27.2
latmax=-26.2
lonmin=-49
lonmax=-48
#
m = Basemap(projection='cyl', resolution='f', llcrnrlon=lonmin, llcrnrlat=latmin , urcrnrlon=lonmax , urcrnrlat=latmax )
fig = plt.figure()
m.drawcoastlines(linewidth=0.25,color = 'k')
m.fillcontinents(color='0.8',lake_color='aqua')
m.plot(lon,lat, 'b.', markersize=10,label=u'Disponível')
m.plot(lon1[13],lat1[11], 'r.', markersize=10,label='CFSR')
#m.plot(-48.651,-26.8833, 'b.', markersize=10,label='METAR') #aeroporto navegantes
plt.title(u'Dados de Vento Analisados',fontsize=12)
plt.legend([u'CFSR',u'METAR'],numpoints=1)
m.drawparallels(np.arange(latmin,latmax,0.5),labels=[1,0,0,0])
m.drawmeridians(np.arange(lonmin,lonmax,0.5),labels=[0,0,0,1])
plt.savefig(dirOut + 'DadosVento_position.png',dpi=200)

