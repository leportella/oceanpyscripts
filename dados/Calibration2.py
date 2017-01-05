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


xy = {
    'local': {
        1: {'x': 68, 'y': 34},
        2: {'x': 73, 'y': 27},
        3: {'x': 138, 'y': 74},
    },
    'reg': {
        1: {'x': 206, 'y': 8},
        2: {'x': 207, 'y': 7},
        3: {'x': 220, 'y': 16},
    }
}

######################### Pontos de Calibração na grade do modelo################
#
# Define ponto pra calcular calibração
k = 1
#
#run = 'run27_run24_fla+chapman'
#grid = 'reg'
#num_files = 1
#data = ReadROMSResults(run, grid, num_files, uv=True)
##
### Encontra o ponto de calibração na grade
#x, y = find_index_of_nearest_xy(
#    data['latr'], 
#    data['lonr'],
#    loc[k]['lat'],
#    loc[k]['lon']
#)



############################### Dados Modelados #################################

run = 'run27_run24_fla+chapman'
grid = 'reg'
num_files = 5
print(datetime.now())
data = ReadROMSResults(run, grid, num_files, x=xy[grid][k]['x'], y=xy[grid][k]['y'], uv=True)
print(datetime.now())


# Pega o dado exclusivo daquele ponto
zeta = data['zeta']
ubar = data['u']
vbar = data['v']

# Arrumando o tempo de referencia pra tempo real e tempo local
refdate = '20110101'
timevector = data['reftime']
data['time'] = FindTimeVector(refdate, timevector)
data['localtime'] = np.subtract(data['time'], timedelta(hours=3))

if len(zeta) == len(ubar) == len(vbar) == len(data['time']) == len(data['localtime']):
    print ('Tudo ok nos dados modelados!')


# Igualando os vetores dos dados modelados e medidos
for i in range(len(data['localtime'])):
    if stsNivel[k]['tempo'][1] == data['localtime'][i]:
        idi= i
        print('idi: ' + str(idi))
    if stsNivel[k]['tempo'][-1] == data['localtime'][i]:
        idf = i
        print('idf: ' + str(idf))
        
tmedido = stsNivel[k]['tempo']
nmedido = stsNivel[k]['previsaottide']
umedido = stsCorr[k]['u_depthav'][1:-1]
vmedido = stsCorr[k]['v_depthav'][1:-1]

if len(tmedido) == len(nmedido) == len(umedido) == len(vmedido):
    print(u'Dados medidos são consistentes')

tmodelado = data['localtime'][idi-1:idf+1]
nmodelado = zeta[idi-1:idf+1]
umodelado = ubar[idi-1:idf+1]
vmodelado = vbar[idi-1:idf+1]

if len(tmodelado) == len(nmodelado) == len(umodelado) == len(vmodelado):
    print(u'Dados modelados são consistentes')

# checks
if len(tmedido) == len(tmodelado):
    print('Vetores de tamanho ok!')
    if tmedido[0] == tmodelado[0]:
        print ('Tempos iniciais ok!')
        if tmedido[1] == tmodelado[1]:
            print('delta t ok!')
            if tmedido[-1] == tmodelado[-1]:
                print('Tempos finais ok!')
                print('Tudo ok! Ok ahead!')

ema_nivel = calcula_ema(nmedido, nmodelado)
remq_nivel = calcula_remq(nmedido, nmodelado)
ia_nivel = calcula_ia(nmedido, nmodelado)

ema_u = calcula_ema(umedido, umodelado)
remq_u = calcula_remq(umedido, umodelado)
ia_u = calcula_ia(umedido, umodelado)

ema_v = calcula_ema(vmedido, vmodelado)
remq_v = calcula_remq(vmedido, vmodelado)
ia_v = calcula_ia(vmedido, vmodelado)


def plota_comparacao_modelado_medido_zeta(save=False):
    plt.figure(figsize=(15,5))
    plt.plot(tmedido,nmedido,'b')
    plt.plot(tmodelado,nmodelado,'r')
    plt.xlabel(u'Tempo')
    plt.ylabel(u'Nível (m)')
    plt.grid()
    plt.legend([u'Valores Medidos', u'Valores Modelados'])
    titulo = u'ST00' + str(k) + ' - EMA: %.2f  REMQ: %.2f  IA: %.2f' % (ema_nivel, remq_nivel, ia_nivel)
    plt.title(titulo)
    if save:
        name = '{}/Calibracao_{}_ST00{}_Nivel.png'.format(dirOut, run, k)
        plt.savefig(name, dpi=200)
    plt.close()
    print('ok')

def plota_comparacao_modelado_medido_uv(save=False):
    plt.figure(figsize=(15,5))
    plt.plot(tmedido,umedido,'b')
    plt.plot(tmodelado,umodelado,'r')
    plt.xlabel(u'Tempo')
    plt.ylabel(u'Velocidade - Componente U (m/s)')
    plt.grid()
    plt.legend([u'Valores Medidos', u'Valores Modelados'])
    titulo = u'ST00' + str(k) + ' - EMA: %.2f  REMQ: %.2f  IA: %.2f'  % (ema_u, remq_u, ia_u)
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
    titulo = u'ST00' + str(k) + ' - EMA: %.2f  REMQ: %.2f  IA: %.2f'  % (ema_v, remq_v, ia_v)
    plt.title(titulo)
    if save:
        name = '{}/Calibracao_{}_ST00{}_V.png'.format(dirOut, run, k)
        plt.savefig(name, dpi=200)
    plt.close()

plota_comparacao_modelado_medido_zeta(save=True)
plota_comparacao_modelado_medido_uv(save=True)


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


