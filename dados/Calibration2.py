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
dirOut = '/home/leportella/Documents/master/dissertacao/Latex/dis_controlada/figuras/Calibracao/'


############################### Dados Medidos ###################################
runfile('/home/leportella/scripts/pyscripts/myscripts/open/DadosNivelTemp.py', wdir='/home/leportella/scripts/pyscripts/myscripts')
stsNivel = sts

runfile('/home/leportella/scripts/pyscripts/myscripts/open/DadosCorrente.py', wdir='/home/leportella/scripts/pyscripts/myscripts')
stsCorr = sts

loc = {k: None for k in range(1, 4)}

loc[1] = {'lat': -26.7682, 'lon': -48.6543}
loc[2] = {'lat': -26.7643, 'lon': -48.6617}
loc[3] = {'lat': -26.7051, 'lon': -48.6157}

del sts
del penha
############################### Dados Modelados #################################
#runs = ['Regional01']
#grade = 'reg'

run = 'Run01a'
grade = 'local'

for run in runs:

    r = nc.Dataset('/home/leportella/cluster/run/' + run + '/ocean_his_' + grade + '.nc','r')
    
    lonr = np.array(r.variables['lon_rho'][:])
    latr = np.array(r.variables['lat_rho'][:])
    otime = np.array(r.variables['ocean_time'][:])
#    maskr = np.array(r.variables['mask_rho'][:])

    ######################### Pontos de Calibração na grade do modelo################
    modelo = {k: None for k in range(1, 4)}
    
    for k in range(1,4):
        y, x = find_index_of_nearest_xy(latr,lonr,loc[1]['lat'],loc[1]['lon'])
        modelo[k] = {'nivel': np.squeeze(r.variables['zeta'][:,y,x])}
        modelo[k]['ubar'] = np.squeeze(r.variables['ubar_eastward'][:,y,x])
        modelo[k]['vbar'] = np.squeeze(r.variables['vbar_northward'][:,y,x])
        
        #calcula o tempo
        modelo[k]['tempo']=[]
        initdate=datetime.datetime(2011,1,1,0,0,0) 
        for t in otime:
            modelo[k]['tempo'].append(np.add(initdate,datetime.timedelta(seconds=int(t))))
        
        modelo[k]['tempo_local']=np.subtract(modelo[k]['tempo'],datetime.timedelta(hours=3))
    
        #igualando os vetores 
        for i in range(len(modelo[k]['tempo'])):
            if stsNivel[k]['tempo'][1]==modelo[k]['tempo'][i]:
                idi= i
        
        for i in range(len(stsNivel[k]['tempo'])):
            if modelo[1]['tempo'][-1]==stsNivel[k]['tempo'][i]:
                idf = i
                           
        tmedido = stsNivel[k]['tempo'][1:idf+1]
        nmedido = stsNivel[k]['previsaottide'][1:idf+1]
        umedido = stsCorr[k]['u_depthav'][1:idf+1]        
        vmedido = stsCorr[k]['v_depthav'][1:idf+1]    
        
        tmodelado = modelo[k]['tempo_local'][idi::]
        nmodelado = modelo[k]['nivel'][idi::]
        umodelado = modelo[k]['ubar'][idi::]
        vmodelado = modelo[k]['vbar'][idi::]
        
        ema = calcula_ema(nmedido,nmodelado)
        remq = calcula_remq(nmedido,nmodelado)
        ia = calcula_ia(nmedido,nmodelado)
        
        plt.figure(figsize=(15,5))
        plt.plot(tmedido,nmedido,'b')
        plt.plot(tmodelado,nmodelado,'r')
        plt.xlabel(u'Tempo')
        plt.ylabel(u'Nível (m)')
        plt.grid()
        plt.legend([u'Valores Medidos', u'Valores Modelados'])
        titulo = u'ST00' + str(k) + ' - EMA: %.2f  REMQ: %.2f  IA: %.2f'  % (ema, remq,ia)
        plt.title(titulo)
        plt.savefig(dirOut + 'Calibracao_' + run + 'ST00' + str(k) + '_Nivel.png', dpi=200)
        
        plt.figure(figsize=(15,5))
        plt.plot(tmedido,umedido,'b')
        plt.plot(tmodelado,umodelado,'r')
        plt.xlabel(u'Tempo')
        plt.ylabel(u'Velocidade - Componente U (m/s)')
        plt.grid()
        plt.legend([u'Valores Medidos', u'Valores Modelados'])
        titulo = u'ST00' + str(k) + ' - EMA: %.2f  REMQ: %.2f  IA: %.2f'  % (ema, remq,ia)
        plt.title(titulo)
        plt.savefig(dirOut + 'Calibracao_' + run + 'ST00' + str(k) + '_U.png', dpi=200)
        
        plt.figure(figsize=(15,5))
        plt.plot(tmedido,vmedido,'b')
        plt.plot(tmodelado,vmodelado,'r')
        plt.xlabel(u'Tempo')
        plt.ylabel(u'Velocidade - Componente v (m/s)')
        plt.grid()
        plt.legend([u'Valores Medidos', u'Valores Modelados'])
        titulo = u'ST00' + str(k) + ' - EMA: %.2f  REMQ: %.2f  IA: %.2f'  % (ema, remq,ia)
        plt.title(titulo)
        plt.savefig(dirOut + 'Calibracao_' + run + '_ST00' + str(k) + '_v.png', dpi=200)

#k=1
#plt.figure(figsize=(15,5))
#plt.plot(sts[k]['tempo'],sts[k]['previsaottide'],'b')
#plt.plot(modelo[k]['tempo_local'],modelo[k]['nivel'],'r')
#plt.xlabel(u'Tempo')
#plt.ylabel(u'Nível (m)')
#plt.grid()
#plt.legend([u'Valores Medidos', u'Valores Modelados'])
##titulo = u'ST00' + str(k) + ' - EMA: %.2f  REMQ: %.3f  IA: %.2f'  % (ema, remq,ia)
#plt.title(titulo)


########################## Plota Pontos ############################
#m = Basemap(projection='cyl', resolution='f', llcrnrlon= -48.7, llcrnrlat= -26.8, urcrnrlon= -48.55, urcrnrlat= -26.65)
#
#fig = plt.figure()
#m.drawcoastlines(linewidth=0.25,color = 'k')
#m.fillcontinents(color='0.8',lake_color='aqua')
#for k in range(1,4):
#    m.plot(loc[k]['lon'],loc[k]['lat'], 'bo', markersize=10,label='Ponto Medido')
#    m.plot(lonr[y,x],latr[y,x], 'ro', markersize=5, label = 'Ponto Avaliado')
#leg = plt.legend(['Dado Medido','Dado Avaliado'],numpoints=1)
##m.legend()


#fig = plt.figure()
#m.drawcoastlines(linewidth=0.25,color = 'k')
#m.fillcontinents(color='0.8',lake_color='aqua')
#m.plot(lonr,latr, 'r.', markersize=5,label='Ponto Medido')
#for k in range(1,4):
#     m.plot(modelo[k]['lon'],modelo[k]['lat'], 'bo', markersize=5, label = 'Ponto Avaliado')
######################### Calcula Model Time ############################

del i
del k
del t

