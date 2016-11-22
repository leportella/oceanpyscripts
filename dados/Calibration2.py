# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 19:16:05 2016
@author: leportella
Calibration of Model
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
          'dis_controlada/figuras/Calibracao')

############################### Dados Medidos ###################################
execfile('/home/leportella/scripts/py/my/oceanpy/dados/DadosNivelTemp.py')
stsNivel = sts

execfile('/home/leportella/scripts/py/my/oceanpy/dados/DadosCorrente.py')
stsCorr = sts

loc = {k: None for k in range(1, 4)}

loc[1] = {'lat': -26.7682, 'lon': -48.6543}
loc[2] = {'lat': -26.7643, 'lon': -48.6617}
loc[3] = {'lat': -26.7051, 'lon': -48.6157} #(737213.8175838569, 7044008.028375013)

############################### Dados Modelados #################################

run = 'run10_regional2_mare'
grid = 'local'
num_files = 2

data = ReadROMSResults(run, grid, num_files, uv=False)

######################### Pontos de Calibração na grade do modelo################

# Define ponto pra calcular calibração
k = 3

# Encontra o ponto de calibração na grade
x, y = find_index_of_nearest_xy(
    data['latr'],
    data['lonr'],
    loc[k]['lat'],
    loc[k]['lon']
)

# Pega o dado exclusivo daquele ponto
zeta = data['zeta'][:, x, y]
# ubar = data['ubar'][:, x, y]
# vbar = data['vbar'][:, x, y]


# Arrumando o tempo de referencia pra tempo real e tempo local
refdate = '20110101'
timevector = data['reftime']
data['time'] = FindTimeVector(refdate, timevector)
data['localtime'] = np.subtract(time, timedelta(hours=3))

# Igualando os vetores dos dados modelados e medidos
for i in range(len(data['time'])):
    if stsNivel[k]['tempo'][1] == data['localtime'][i]:
        idi= i

for i in range(len(stsNivel[k]['tempo'])):
    if data['localtime'][-1] == stsNivel[k]['tempo'][i]:
        idf = i

tmedido = stsNivel[k]['tempo'][1:idf+1]
nmedido = stsNivel[k]['previsaottide'][1:idf+1]
umedido = stsCorr[k]['u_depthav'][1:idf+1]
vmedido = stsCorr[k]['v_depthav'][1:idf+1]

tmodelado = data['localtime'][idi::]
nmodelado = zeta[idi::]
umodelado = ubar[idi::]
vmodelado = vbar[idi::]

ema = calcula_ema(nmedido, nmodelado)
remq = calcula_remq(nmedido, nmodelado)
ia = calcula_ia(nmedido, nmodelado)


plota_comparacao_modelado_medido_zeta()




def plota_comparacao_modelado_medido_zeta(save=False):
    plt.figure(figsize=(15,5))
    plt.plot(tmedido,nmedido,'b')
    plt.plot(tmodelado,nmodelado,'r')
    plt.xlabel(u'Tempo')
    plt.ylabel(u'Nível (m)')
    plt.grid()
    plt.legend([u'Valores Medidos', u'Valores Modelados'])
    titulo = u'ST00' + str(k) + ' - EMA: %.2f  REMQ: %.2f  IA: %.2f'  % (ema, remq, ia)
    plt.title(titulo)
    if save:
        name = '{}/Calibracao_{}_ST00{}_Nivel.png'.format(dirOut, run, k)
        plt.savefig(name, dpi=200)
    plt.close()

def plota_comparacao_modelado_medido_uv(save=False):
    plt.figure(figsize=(15,5))
    plt.plot(tmedido,umedido,'b')
    plt.plot(tmodelado,umodelado,'r')
    plt.xlabel(u'Tempo')
    plt.ylabel(u'Velocidade - Componente U (m/s)')
    plt.grid()
    plt.legend([u'Valores Medidos', u'Valores Modelados'])
    titulo = u'ST00' + str(k) + ' - EMA: %.2f  REMQ: %.2f  IA: %.2f'  % (ema, remq,ia)
    plt.title(titulo)
    if save:
        name = '{}/Calibracao_{}_ST00{}_U.png'.format(dirOut, run, k)
        plt.savefig(name, dpi=200)
    plt.close()

    plt.figure(figsize=(15,5))
    plt.plot(tmedido,vmedido,'b')
    plt.plot(tmodelado,vmodelado,'r')
    plt.xlabel(u'Tempo')
    plt.ylabel(u'Velocidade - Componente v (m/s)')
    plt.grid()
    plt.legend([u'Valores Medidos', u'Valores Modelados'])
    titulo = u'ST00' + str(k) + ' - EMA: %.2f  REMQ: %.2f  IA: %.2f'  % (ema, remq,ia)
    plt.title(titulo)
    if save:
        name = '{}/Calibracao_{}_ST00{}_V.png'.format(dirOut, run, k)
        plt.savefig(name, dpi=200)
    plt.close()


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


