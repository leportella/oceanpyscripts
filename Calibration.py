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
#from ncwork import *
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import datetime 
from estatisticatools import *

direct = '/home/leportella/Documents/master/dados/utilizacao/'
dirOut = '/home/leportella/Documents/master/dissertacao/Latex/dis_controlada/figuras/'


############################### Dados Medidos ###################################
loc = {k: None for k in range(1, 4)}

loc[1] = {'lat': -26.7682, 'lon': -48.6543}
loc[2] = {'lat': -26.7643, 'lon': -48.6617}
loc[3] = {'lat': -26.7051, 'lon': -48.6157}

############################### Dados Modelados #################################
runs = {'Regional01'}
#runs = {'Run01a'}

for run in runs:

    r = nc.Dataset('/home/leportella/cluster/run/' + run + '/ocean_his_reg.nc','r')
    
    lonr = np.array(r.variables['lon_rho'][:])
    latr = np.array(r.variables['lat_rho'][:])
    otime = np.array(r.variables['ocean_time'][:])
    
    ######################### Pontos de Calibração na grade do modelo################
    modelo = {k: None for k in range(1, 4)}
    
    for k in range(1,4):
        rowlat, collat = FindSimilar(loc[k]['lat'],latr)
        rowlon, collon = FindSimilar(loc[k]['lon'],lonr)
    #    #pontos de calibração real no modelo
        modelo[k] = {'lat': latr[rowlat,collat]}
        modelo[k]['lon']= lonr[rowlon,collon]
        modelo[k]['nivel']= np.squeeze(r.variables['zeta'][:,rowlat,collon])
        
    #    #calcula o tempo
        modelo[k]['tempo']=[]
        initdate=datetime.datetime(2011,1,1,0,0,0) 
        for t in otime:
            modelo[k]['tempo'].append(np.add(initdate,datetime.timedelta(seconds=int(t))))
        
        modelo[k]['tempo_local']=np.subtract(modelo[k]['tempo'],datetime.timedelta(hours=3))
#    
#        #igualando os vetores 
#        for i in range(len(modelo[k]['tempo'])):
#            if sts[k]['tempo'][1]==modelo[k]['tempo'][i]:
#                idi= i
#        
#        for i in range(len(sts[k]['tempo'])):
#            if modelo[1]['tempo'][-1]==sts[k]['tempo'][i]:
#                idf = i
#                           
#        tmedido = sts[k]['tempo'][1:idf+1:2]
#        nmedido = sts[k]['previsaottide'][1:idf+1:2]
#        
#        tmodelado = modelo[k]['tempo_local'][idi::]
#        nmodelado = modelo[k]['nivel'][idi::]
#        
#        ema = calcula_ema(nmedido,nmodelado)
#        remq = calcula_remq(nmedido,nmodelado)
#        ia = calcula_ia(nmedido,nmodelado)
#        
#        plt.figure(figsize=(15,5))
#        plt.plot(tmedido,nmedido,'b')
#        plt.plot(tmodelado,nmodelado,'r')
#        plt.xlabel(u'Tempo')
#        plt.ylabel(u'Nível (m)')
#        plt.grid()
#        plt.legend([u'Valores Medidos', u'Valores Modelados'])
#        titulo = u'ST00' + str(k) + ' - EMA: %.2f  REMQ: %.3f  IA: %.2f'  % (ema, remq,ia)
#        plt.title(titulo)
#        plt.savefig(dirOut + 'Calibracao_' + run + 'ST00' + str(k) + '.png', dpi=200)

k=1
plt.figure(figsize=(15,5))
plt.plot(sts[k]['tempo'],sts[k]['previsaottide'],'b')
plt.plot(modelo[k]['tempo_local'],modelo[k]['nivel'],'r')
plt.xlabel(u'Tempo')
plt.ylabel(u'Nível (m)')
plt.grid()
plt.legend([u'Valores Medidos', u'Valores Modelados'])
#titulo = u'ST00' + str(k) + ' - EMA: %.2f  REMQ: %.3f  IA: %.2f'  % (ema, remq,ia)
#plt.title(titulo)


########################## Plota Pontos ############################
#m = Basemap(projection='cyl', resolution='f', llcrnrlon= -48.7, llcrnrlat= -26.8, urcrnrlon= -48.55, urcrnrlat= -26.65)
#
#fig = plt.figure()
#m.drawcoastlines(linewidth=0.25,color = 'k')
#m.fillcontinents(color='0.8',lake_color='aqua')
#for k in range(1,4):
#    m.plot(loc[k]['lon'],loc[k]['lat'], 'bo', markersize=10,label='Ponto Medido')
#    m.plot(modelo[k]['lon'],modelo[k]['lat'], 'ro', markersize=5, label = 'Ponto Avaliado')
#leg = plt.legend(['Dado Medido','Dado Avaliado'],numpoints=1)
##m.legend()


#fig = plt.figure()
#m.drawcoastlines(linewidth=0.25,color = 'k')
#m.fillcontinents(color='0.8',lake_color='aqua')
#m.plot(lonr,latr, 'r.', markersize=5,label='Ponto Medido')
#for k in range(1,4):
#     m.plot(modelo[k]['lon'],modelo[k]['lat'], 'bo', markersize=5, label = 'Ponto Avaliado')
######################### Calcula Model Time ############################