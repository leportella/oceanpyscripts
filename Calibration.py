# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 19:16:05 2016

@author: leportella
"""
import sys

sys.path.insert(0,'/home/leportella/scripts/pyscripts/myscripts/open')

import netCDF4 as nc
import numpy as np
from generaltools import *
from ncwork import *
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap
import datetime 

direct = '/home/leportella/Documents/master/dados/utilizacao/'
dirOut = '/home/leportella/Documents/master/dissertacao/Latex/dis_controlada/figuras/'


############################### Dados Medidos ###################################
#sts = {k: None for k in range(1, 4)}
loc = {k: None for k in range(1, 4)}
#for k in range(1,4):
#    sts[k] = pd.read_csv(direct+'DF_NivelTemp_' + str (k) + '.csv')


loc[1] = {'lat': -26.7682, 'lon': -48.6543}
loc[2] = {'lat': -26.7643, 'lon': -48.6617}
loc[3] = {'lat': -26.7051, 'lon': -48.6157}

############################### Dados Modelados #################################
r = nc.Dataset('/home/leportella/cluster/testes_iniciais/teste09/ocean_his_local.nc','r')
lonr = np.array(r.variables['lon_rho'][:])
latr = np.array(r.variables['lat_rho'][:])
zeta = r.variables['zeta'][:]
otime = np.array(r.variables['ocean_time'][:])

######################### Pontos de Calibração na grade do modelo################

for k in range(1,4):
    rowlat, collat = FindSimilar(loc[k]['lat'],latr)
    rowlon, collon = FindSimilar(loc[k]['lon'],lonr)
    loc[k]['calibration_id']= rowlat,collat,rowlon,collon
    #pontos de calibração real no modelo
    loc[k]['calpt_lat']=latr[rowlat,collat]
    loc[k]['calpt_lon']=lonr[rowlon,collon]
    loc[k]['nivelmodelado']=zeta[:,rowlat,collon]
    
######################### Plota Pontos ############################
#m = Basemap(projection='cyl', resolution='f', llcrnrlon= -48.7, llcrnrlat= -26.8, urcrnrlon= -48.55, urcrnrlat= -26.65)
#
#fig = plt.figure()
#m.drawcoastlines(linewidth=0.25,color = 'k')
#m.fillcontinents(color='0.8',lake_color='aqua')
#for k in range(1,4):
#    m.plot(loc[k]['lon'],loc[k]['lat'], 'bo', markersize=10,label='Ponto Medido')
#    m.plot(loc[k]['calpt_lon'],loc[k]['calpt_lat'], 'ro', markersize=5, label = 'Ponto Avaliado')
#leg = plt.legend(['Dado Medido','Dado Avaliado'],numpoints=1)
#m.legend()

######################### Calcula Model Time ############################
mtime=[]
initdate=datetime.datetime(2011,1,1,0,0,0) 
for t in otime:
    mtime.append(np.add(initdate,datetime.timedelta(seconds=int(t))))

mtimelocal=np.subtract(mtime,datetime.timedelta(hours=3))

plt.figure(figsize=(15,5))
plt.plot(sts[3]['tempo'],sts[3]['previsaottide'],'b')
plt.plot(mtimelocal,loc[3]['nivelmodelado'],'r')
plt.xlabel(u'Tempo')
plt.ylabel(u'Nível (m)')
plt.grid()
plt.legend([u'Valores Medidos', u'Valores Modelados'])
plt.title(u'Nível - ST003')
plt.savefig(dirOut + 'Calibracao_Teste09.png',dpi=200)

#

