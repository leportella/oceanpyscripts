#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.insert(0,'/home/leportella/scripts/py/my/oceanpy/tools/')
sys.path.insert(0,'/home/leportella/scripts/py/ttide_py-master/ttide')

from generaltools import *
from ttide.t_tide import t_tide
import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import numpy.fft as fft
import pandas as pd


direct = '/home/leportella/Documents/master/dados/utilizacao/'
dirOut = '/home/leportella/Documents/master/dissertacao/Latex/dis_controlada/figuras/'

###############################################################################
##                                                                           ##
##                     ADCPS PIÇARRAS DAT                                    ##
##                                                                           ##
###############################################################################

# Reading the files
ST001 = np.array(
    list(
        csv.reader(open(direct+'ST001_Nivel_Temp.csv','rb'), delimiter=';')
    )[1:],dtype=np.float64)
ST002 = np.array(
    list(
        csv.reader(open(direct+'ST002_Nivel_Temp.csv','rb'), delimiter=',')
    )[1:],dtype=np.float64)
ST003 = np.array(
    list(
        csv.reader(open(direct+'ST003_Nivel_Temp.csv','rb'), delimiter=',')
    )[1:],dtype=np.float64)

STs = {1: ST001, 2: ST002, 3: ST003}
sts = {k: None for k in range(1, 4)}

# Organizing all the data in single variables

for k in range(1,4):
    t=[]
    rep = STs[k]

    # creating a datenum vector for time
    for i in range(0,len(rep)):
        t.append(
            datetime.datetime(
                int(rep[i,0]), int(rep[i,1]), int(rep[i,2]),
                int(rep[i,3]), int(rep[i,4]), int(rep[i,5])
            )
        )

    # the third equipment is in UTC that should be considered
    if k==3:
        temp=np.subtract(t,datetime.timedelta(hours=3))
        sts[k] = {'tempo': temp}
    else:
        sts[k] = {'tempo': t}

    sts[k]['nivel'] = pd.Series(rep[:,6])
    sts[k]['temp'] = pd.Series(rep[:,7])


    # we should disconsider the unknown values represented by 999
    nodata = []
    # retreving the points were there is no available data
    for n in range(len(sts[k]['nivel'])):
        if sts[k]['nivel'][n] == 999:
            nodata.append(n)
    sts[k]['nodata_ids'] = nodata

    # changing non available data to NaN
    sts[k]['nivel'][sts[k]['nivel']==999] = np.nan
    sts[k]['temp'][sts[k]['temp']==999] = np.nan

    # linear interpolation of vectors to populate missing data
    sts[k]['nivelinterp'] = sts[k]['nivel'].interpolate()
    sts[k]['tempinterp'] = sts[k]['temp'].interpolate()

    # calculate general statistcs for waterlevel data
    sts[k]['media_nivel'] = np.mean(sts[k]['nivel'])
    sts[k]['mediana_nivel'] = np.median(sts[k]['nivel'])
    sts[k]['max_nivel'] = np.max(sts[k]['nivel'])
    sts[k]['min_nivel'] = np.min(sts[k]['nivel'])
    sts[k]['std_nivel'] = np.std(sts[k]['nivel'])

    # calculate general statistics for temperature data
    sts[k]['media_temp'] = np.mean(sts[k]['temp'])
    sts[k]['mediana_temp'] = np.median(sts[k]['temp'])
    sts[k]['max_temp'] = np.max(sts[k]['temp'])
    sts[k]['min_temp'] = np.min(sts[k]['temp'])
    sts[k]['std_temp'] = np.std(sts[k]['temp'])

    # calculates fast fourier transform for waterlevel data
    sts[k]['spectrum']=fft.fft(sts[k]['nivelinterp'][0::2])
    sts[k]['freq'] = fft.fftfreq(len(sts[k]['spectrum']))

    sts[k]['tspectrum']=fft.fft(sts[k]['tempinterp'][0::2])
    sts[k]['tfreq'] = fft.fftfreq(len(sts[k]['tspectrum']))

    # applying t_tide calculations to get harmonic constants on
    # waterlevel data
    ttide_analysis =  t_tide(
        (sts[k]['nivelinterp']-sts[k]['media_nivel'])*100,
        dt=0.5,
        lat=np.array(-25)
    )
    sts[k]['nameu1'], sts[k]['fu1'], sts[k]['tideconout1'], sts[k]['xout1'] = ttide_analyis  # noqa

    # select tide astronomic signal in cm
    sts[k]['previsaottide'] = sts[k]['xout1'].squeeze()/100


###############################################################################
##                                                                           ##
##                CREATING FIGURES                                           ##
##                                                                           ##
###############################################################################



















######################### fft com eixo em log ####################################
#plt.figure(figsize=(15,5))
#plt.semilogx(sts[1]['freq'], sts[1]['spectrum'])
#plt.semilogx(sts[2]['freq'], sts[2]['spectrum'],'r')
#plt.semilogx(sts[3]['freq'], sts[3]['spectrum'],'g')
#plt.xlim(0.01,0.2)
#plt.ylim(0,100)
#plt.xlabel(u'Frequência')
#plt.xticks(np.arange(min(0.01), max(0.2), 1))
#plt.grid()
#plt.legend(['ST001', 'ST002','ST003'])
#plt.title(u'Espectro da Maré - Piçarras 2011')
#plt.savefig(dirOut + 'Espectro_FFT_Picarras_Logx.png',dpi=200)
#
######################### fft com eixo x normal###################################
#plt.figure(figsize=(15,5))
#plt.plot(sts[1]['freq'], sts[1]['spectrum'])
#plt.plot(sts[2]['freq'], sts[2]['spectrum'],'r')
#plt.plot(sts[3]['freq'], sts[3]['spectrum'],'g')
#plt.xlim(0.001,0.2)
#plt.ylim(0,100)
#plt.xlabel(u'Frequência')
#plt.grid()
#plt.legend(['ST001', 'ST002','ST003'])
#plt.title(u'Espectro da Maré - Piçarras 2011')
#plt.savefig(dirOut + 'Espectro_FFT_Picarras_Plot.png',dpi=200)

######################## nivel normalizado ######################################
#plt.figure(figsize=(15,5))
#plt.plot(sts[1]['tempo'], sts[1]['nivelinterp']-sts[1]['media_nivel'])
#plt.plot(sts[2]['tempo'], sts[2]['nivelinterp']-sts[2]['media_nivel'],'r')
#plt.plot(sts[3]['tempo'], sts[3]['nivelinterp']-sts[3]['media_nivel'],'g')
#plt.xlabel(u'Tempo')
#plt.ylabel(u'Nível (m)')
#plt.grid()
#plt.legend(['ST001', 'ST002','ST003'])
#plt.title(u'Nível - Piçarras 2011')
#plt.savefig(dirOut + 'Nivel_Normalizado_Picarras.png',dpi=200)

######################### nivel original ######################################
#a = np.isnan(sts[1]['nivel'])
#b=np.logical_not(a)
#tempo_temporario = sts[1]['tempo'][a].values
#
#plt.figure(figsize=(15,5))
#plt.plot(sts[1]['tempo'][b], (sts[1]['nivel']-sts[1]['media_nivel'])[b],'.')
#plt.plot(tempo_temporario, np.zeros(len(tempo_temporario)),'.r')
##plt.plot(sts[1]['tempo'][sts[1]['nivel']==np.nan],sts[1]['nivel'][sts[1]['nivel']==np.nan],'.r')
##plt.plot(sts[2]['tempo'], sts[2]['nivelinterp']-sts[2]['media_nivel'],'r')
##plt.plot(sts[3]['tempo'], sts[3]['nivelinterp']-sts[3]['media_nivel'],'g')
#plt.xlabel(u'Tempo')
#plt.ylabel(u'Nível (m)')
#plt.grid()
#plt.legend([u'Valores Medidos', u'Valores Não Medidos'])
#plt.title(u'Nível - ST001')
#plt.savefig(dirOut + 'Nivel_ExemploNans.png',dpi=200)
#
######################### nivel medido e previsto pelo ttide #################################

#fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, sharey=True, sharex=True, figsize=(11, 5))
#
##fig.suptitle(u'Nível (m)', fontsize=14)
#ax0.plot(sts[1]['tempo'], sts[1]['nivelinterp']-sts[1]['media_nivel'], label=u'ST001')
#ax0.plot(sts[2]['tempo'], sts[2]['nivelinterp']-sts[2]['media_nivel'],'r', label=u'ST002')
#ax0.plot(sts[3]['tempo'], sts[3]['nivelinterp']-sts[3]['media_nivel'],'g', label=u'ST003')
#ax0.legend(numpoints=3, bbox_to_anchor=(1.13, 1),fontsize = 'small')
#ax0.set_title("Dados Medidos")
#ax0.grid()
#
#ax1.plot(sts[1]['tempo'], sts[1]['previsaottide'], alpha=0.5, label=u'ST001')
#ax1.plot(sts[2]['tempo'], sts[2]['previsaottide'], 'r', alpha=0.5, label=u'ST002')
#ax1.plot(sts[3]['tempo'], sts[3]['previsaottide'], 'g', alpha=0.5, label=u'ST003')
#ax1.legend(numpoints=3, bbox_to_anchor=(1.13, 1),fontsize = 'small')
#ax1.set_title("Dados Previstos")
#ax1.grid()
#
#ax2.plot(sts[1]['tempo'], sts[1]['nivelinterp']-sts[1]['media_nivel']-sts[1]['previsaottide'], alpha=0.5, label=u'ST001')
#ax2.plot(sts[2]['tempo'], sts[2]['nivelinterp']-sts[2]['media_nivel']-sts[2]['previsaottide'],'r', alpha=0.5, label=u'ST002')
#ax2.plot(sts[3]['tempo'], sts[3]['nivelinterp']-sts[3]['media_nivel']-sts[3]['previsaottide'], 'g', alpha=0.5, label=u'ST003')
#ax2.legend(numpoints=3, bbox_to_anchor=(1.13, 1),fontsize = 'small')
#ax2.set_title(u"Resíduo")
#ax2.grid()
#
#plt.savefig(dirOut + 'Nivel_Previsao_Geral.png',dpi=300)




#################################################################################
##                                                                             ##
##                          NIVEL DE PENHA                                     ##
##                                                                             ##
#################################################################################


Penha=np.array(list(csv.reader(open(direct+'maregrafo_penha.csv','rb'),delimiter=',')),dtype=np.float64)

t=[]
for i in range(0,len(Penha)):
    t.append(datetime.datetime(int(Penha[i,2]),int(Penha[i,1]),int(Penha[i,0]),int(Penha[i,3]),int(Penha[i,4]),int(Penha[i,5])))

penha={'tempo':pd.Series(t)}
penha['nivel']=pd.Series(Penha[:,6]/100)

n=np.array(pd.Series(Penha[:,6]))


penha['spectrum']=abs(fft.fft(penha['nivel']))
penha['freq'] = fft.fftfreq(len(penha['spectrum']))
penha['nameu1'], penha['fu1'], penha['tideconout1'], penha['xout1'] = t_tide(n, dt=1, lat=np.array(-25))

penha['xout1']=penha['xout1']/100






######################### Plot Nivel Penha ####################################
#plt.figure(figsize=(15,5))
#plt.plot(penha['tempo'],penha['nivel'])
#plt.title(u'Nível - Penha')
#plt.ylabel(u'Nível (m)')
#plt.grid()
#plt.savefig(dirOut + 'Nivel_Penha.png',dpi=200)

################################# fft Penha ####################################
#plt.figure(figsize=(15,5))
#plt.plot(penha['freq'], penha['spectrum'])
#plt.xlim(0.001,0.2)
#plt.xlabel(u'Frequência')
#plt.grid()
#plt.title(u'Espectro da Maré - Penha 95-96')
#plt.savefig(dirOut + 'Espectro_FFT_Penha.png',dpi=200)


########################## fft Penha e PIçarra juntas ####################################
#fig, (ax0, ax1) = plt.subplots(nrows=2, sharey=False, sharex=True, figsize=(11, 5))
#
#sts[1]['period'] = np.divide(1, sts[1]['freq'])
#sts[2]['period'] = np.divide(1, sts[2]['freq'])
#sts[3]['period'] = np.divide(1, sts[3]['freq'])
#penha['period'] = np.divide(1, penha['freq'])
#
#ax0.plot(sts[1]['period'], sts[1]['spectrum'])
#ax0.plot(sts[2]['period'], sts[2]['spectrum'],'r')
#ax0.plot(sts[3]['period'], sts[3]['spectrum'],'g')
#ax0.grid()
#ax0.set_ylim(0,100)
#ax0.set_xlim(0.001,30)
#
#ax0.set_title(u"Espectro de Energia - Piçarras")
#ax0.legend(['ST001', 'ST002','ST003'])
#
#ax1.plot(penha['period'], penha['spectrum'])
#ax1.set_title(u"Espectro de Energia - Penha")
#ax1.set_ylim(0,1600)
#ax1.set_xlim(0.001,30)
#ax1.set_xlabel(u'Período em Horas')
#ax1.grid()
#
#plt.savefig(dirOut + 'Espectro_FFT_Penha_Periodo.png',dpi=200)


########################## fft Penha e PIçarra juntas  LOG LOG ####################################
fig, (ax0, ax1) = plt.subplots(nrows=2, sharey=False, sharex=True, figsize=(11, 5))

sts[1]['period'] = np.divide(1, sts[1]['freq'])
sts[2]['period'] = np.divide(1, sts[2]['freq'])
sts[3]['period'] = np.divide(1, sts[3]['freq'])
penha['period'] = np.divide(1, penha['freq'])

ax0.loglog(sts[1]['period'], sts[1]['spectrum'])
ax0.loglog(sts[2]['period'], sts[2]['spectrum'],'r')
ax0.loglog(sts[3]['period'], sts[3]['spectrum'],'g')
ax0.grid()
ax0.set_ylim(10**-3,10**3)
ax0.set_xlim(10*0, 10**2)

ax0.set_title(u"Espectro de Energia - Piçarras")
ax0.legend(['ST001', 'ST002','ST003'])

ax1.loglog(penha['period'], penha['spectrum'])
ax1.set_title(u"Espectro de Energia - Penha")
ax1.set_ylim(10**-3,10**4)
ax1.set_xlim(10*0, 10**2)

ax1.set_xlabel(u'Período em Horas')
ax1.grid()

plt.savefig(dirOut + 'Espectro_FFT_Penha_Periodo_loglog.png',dpi=200)



######################### MareMeteorologica Negativa em PIçarras ####################################
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, sharey=True, sharex=True,
                                    figsize=(11, 5))

ax0.plot(penha['tempo'], penha['nivel'], label=u'Penha')
ax0.plot(penha['tempo'][80], penha['nivel'][80], 'ro', label=u'Início')
ax0.plot(penha['tempo'][152], penha['nivel'][152], 'go', label=u'Fim')
ax0.legend(numpoints=1, bbox_to_anchor=(1.13, 1),fontsize = 'small')
ax0.set_title("Dados Medidos")
ax0.set_ylabel(u'Nível (m)')
ax0.grid()

ax1.plot(penha['tempo'], penha['xout1'], alpha=0.5, label=u'Penha')
ax1.plot(penha['tempo'][80], penha['xout1'][80], 'ro', label=u'Início')
ax1.plot(penha['tempo'][152], penha['xout1'][152], 'go', label=u'Fim')
ax1.legend(numpoints=1, bbox_to_anchor=(1.13, 1),fontsize = 'small')
ax1.set_title("Dados Previstos")
ax1.grid()
ax1.set_ylabel(u'Nível (m)')


tt = penha['nivel']-penha['xout1'][:,0]
ax2.plot(penha['tempo'], tt, alpha=0.5,
         label=u'Penha')
ax2.plot(penha['tempo'][80], tt[80], 'ro', label=u'Início')
ax2.plot(penha['tempo'][152], tt[152], 'go', label=u'Fim')
ax2.legend(numpoints=1, bbox_to_anchor=(1.13, 1),fontsize = 'small')
ax2.set_title(u"Resíduo")
ax2.grid()
ax2.set_ylabel(u'Nível (m)')
ax2.set_xlabel(u'Tempo')
plt.savefig(dirOut + 'Nivel_Penha_MareMeteoNegativa.png',dpi=300)

##---------------------------------------------
#fig, (ax0, ax1) = plt.subplots(nrows=2, sharey=True, sharex=True, figsize=(11, 5))
#ax0.plot(penha['tempo'], penha['nivel'], label=u'Medido')
#ax0.legend(numpoints=3, bbox_to_anchor=(1.13, 1),fontsize = 'small')
#ax0.set_title("Penha")
#ax0.set_ylabel(u'Nivel (m)')
#ax0.grid()
#
#ax1.plot(penha['tempo'], penha['xout1'], alpha=0.5, label=u'Previsto')
#ax1.plot(penha['tempo'], penha['nivel']-penha['xout1'][:,0], 'r', alpha=0.5, label=u'Resíduo')
#ax1.legend(numpoints=3, bbox_to_anchor=(1.14, 1),fontsize = 'small')
#ax1.set_ylabel(u'Nivel (m)')
#ax1.set_xlabel(u'Tempo')
#ax1.grid()
#plt.savefig(dirOut + 'Nivel_Previsto_Penha2.png',dpi=300)

#################################################################################
##                                                                             ##
##                  PLOT FIGURAS DE TEMP DE PICARRAS                              ##
##                                                                             ##
#################################################################################

#plt.figure(figsize=(15,5))
#plt.plot(sts[1]['tempo'],sts[1]['tempinterp'])
#plt.plot(sts[2]['tempo'][0::2],sts[2]['tempinterp'][0::2],'r')
#plt.plot(sts[3]['tempo'][0::2],sts[3]['tempinterp'][0::2],'g')
#plt.title(u'Temperatura - Piçarras')
#plt.ylabel(u'Temperatura (graus Celsius)')
#plt.grid()
#plt.ylim(17,21)
#plt.legend(['ST001', 'ST002','ST003'],bbox_to_anchor=(1.13, 0.97))
##plt.xlim(st002['tempo'][0], st002['tempo'][50])
#plt.savefig(dirOut + 'Temperatura_Geral.png',dpi=200)


######################## fft com eixo em log ####################################
#plt.figure(figsize=(15,5))
#plt.plot(sts[1]['tfreq'], sts[1]['tspectrum'])
#plt.plot(sts[2]['tfreq'], sts[2]['tspectrum'],'r')
#plt.plot(sts[3]['tfreq'], sts[3]['tspectrum'],'g')
#plt.xlim(0.02,0.4)
#plt.ylim(0,40)
#plt.xlabel(u'Frequência')
#plt.grid()
#plt.legend(['ST001', 'ST002','ST003'])
#plt.title(u'Espectro da Temperatura - Piçarras 2011')
#plt.savefig(dirOut + 'Espectro_FFT_Temp_Picarras.png',dpi=200)


#################################################################################
##                                                                             ##
##                              PLOT TEMP VS VENTO                             ##
##                                                                             ##
#################################################################################


################################# PLOT VELOCIDADE #################################
#fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, sharey=False, sharex=True, figsize=(15, 5))
#fig.suptitle(u'Temperatura', fontsize=14)
#ax0.plot(sts[1]['tempo'],sts[1]['tempinterp'], label=u'ST001')
#ax0.plot(sts[2]['tempo'][0::2],sts[2]['tempinterp'][0::2],'r',label='ST002')
#ax0.plot(sts[3]['tempo'][0::2],sts[3]['tempinterp'][0::2],'g',label='ST002')
#
#ax1.plot(met['tempo'],met['vel'])
#ax1.set_ylim(0,10)
#
#ax2.plot(cfsr['tempo'],cfsr['vel'])
#ax2.set_xlim(sts[1]['tempo'][0], sts[2]['tempo'].iloc[-1])
#ax2.set_ylim(0,10)
#plt.savefig(dirOut + 'Temp_vs_velvento.png',dpi=200)

################################ PLOT DIREÇÃO ## #################################
#fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, sharey=False, sharex=True, figsize=(15, 5))
#fig.suptitle(u'Temperatura', fontsize=14)
#ax0.plot(sts[1]['tempo'],sts[1]['tempinterp'], label=u'ST001')
#ax0.plot(sts[2]['tempo'][0::2],sts[2]['tempinterp'][0::2],'r',label='ST002')
#ax0.plot(sts[3]['tempo'][0::2],sts[3]['tempinterp'][0::2],'g',label='ST002')
#
#ax1.plot(met['tempo'],met['dir'])
#ax1.set_ylim(0,360)
#
#ax2.plot(cfsr['tempo'],cfsr['dir'])
#ax2.set_xlim(sts[1]['tempo'][0], sts[2]['tempo'].iloc[-1])
#ax2.set_ylim(0,360)
#plt.savefig(dirOut + 'Temp_vs_dirvento.png',dpi=200)

######################### TEMPERATURA VS VENTO ####################################
#plt.figure(figsize=(15,5))
#plt.plot(cfsr['tempo'],cfsr['dir'],)
#ax = plt.gca()
#ax2 = ax.twinx()
#ax2.plot(sts[1]['tempo'],sts[1]['tempinterp'],'r')
#plt.xlim(sts[1]['tempo'][1],sts[1]['tempo'][-1])
#ax2.set_ylim(17,21)
#plt.title(u'Temperatura em ST001 e Direçãdo do Vento')
#ax.set_ylabel(u'Direção do Vento (graus)',color='blue')
#ax2.set_ylabel(u'Temperatura (graus Celcius)',color='red')
#plt.grid()
#plt.savefig(dirOut + 'Temperatura_Vento_ST001.png',dpi=200)
#
#
#plt.figure(figsize=(15,5))
#plt.plot(cfsr['tempo'],cfsr['dir'],)
#ax = plt.gca()
#ax2 = ax.twinx()
#ax2.plot(sts[2]['tempo'][0::2],sts[2]['tempinterp'][0::2],'r')
#plt.xlim(sts[2]['tempo'][1],sts[2]['tempo'][-1])
#ax2.set_ylim(17,21)
#plt.title(u'Temperatura em ST002 e Direçãdo do Vento')
#ax.set_ylabel(u'Direção do Vento (graus)',color='blue')
#ax2.set_ylabel(u'Temperatura (graus Celcius)',color='red')
#plt.grid()
#plt.savefig(dirOut + 'Temperatura_Vento_ST002.png',dpi=200)
#
#
#plt.figure(figsize=(15,5))
#plt.plot(cfsr['tempo'],cfsr['dir'],)
#ax = plt.gca()
#ax2 = ax.twinx()
#ax2.plot(sts[3]['tempo'][0::2],sts[3]['tempinterp'][0::2],'r')
#plt.xlim(sts[3]['tempo'][1],sts[3]['tempo'][-1])
#ax.set_ylabel(u'Direção do Vento (graus)',color='blue')
#ax2.set_ylabel(u'Temperatura (graus Celcius)',color='red')
#ax2.set_ylabel(u'Temperatura (graus Celcius)')
#ax2.set_ylim(17,21)
#plt.grid()
#plt.title(u'Temperatura em ST003 e Direçãdo do Vento')
#plt.savefig(dirOut + 'Temperatura_Vento_ST003.png',dpi=200)
#



######################### hISTOGRAA DOS DADOS DE NIVEL ####################################
#for k in range(1,4):
#    PercentHistogram(sts[k]['nivel']-sts[k]['media_nivel'],binss=40)
#    plt.title(u'Histograma dados de Nível - ST00' + str(k))
#    plt.ylabel(u'Percentual')
#    plt.xlabel(u'Nível (m)')
#    plt.xlim(-1.2,1.2)
#    plt.grid()
#    plt.savefig(dirOut + 'Hist_nivel_ST00' + str(k)+'.png',dpi=200)
#
#
#PercentHistogram(penha['nivel'],binss=50)
#plt.title(u'Histograma dados de Nível - Penha')
#plt.ylabel(u'Percentual')
#plt.xlabel(u'Nível (m)')
#plt.xlim(-1.2,1.2)
#plt.grid()
#plt.savefig(dirOut + 'Hist_nivel_Penha.png',dpi=200)



## --------------------------------------------------
k=1
fig, (ax0, ax1) = plt.subplots(nrows=2, sharey=True, sharex=True, figsize=(12, 5))

ax0.plot(sts[k]['tempo'], sts[k]['nivelinterp']-sts[k]['media_nivel'], label=u'Medido')
ax0.legend(numpoints=3, bbox_to_anchor=(1.12, 1),fontsize = 'small')
ax0.set_title("ST00{}".format(k))
ax0.set_ylabel(u'Nível (m)')
ax0.grid()

ax1.plot(sts[k]['tempo'], sts[k]['previsaottide'], alpha=0.5, label=u'Previsto')
ax1.plot(sts[k]['tempo'], sts[k]['nivelinterp']-sts[k]['media_nivel']-sts[k]['previsaottide'],
         'r', alpha=0.5, label=u'Residual')
ax1.legend(numpoints=3, bbox_to_anchor=(1.13, 1),fontsize = 'small')
ax1.set_ylim(-1, 1)
ax1.set_ylabel(u'Nível (m)')
ax1.set_xlabel(u'Tempo')
ax1.grid()

plt.savefig(dirOut + 'Nivel_Previsao_Geral_ST00{}.png'.format(k),dpi=300)

## --------------------------------------------------




#-----------------------------------------------------------------------
#
## Separando a temperatura de acordo com os dados de vento
#
#temperatura = []
#tempo = []
#for i in range(9,len(sts[1]['tempinterp']), 12):
#    temperatura.append(sts[1]['tempinterp'][i])
#    tempo.append(sts[1]['tempo'][i])
#
#vento_tem = cfsr['time'][924:1058+1]
#vento_dir = cfsr['dir'][924:1058+1]
#vento_vel = cfsr['vel'][924:1058+1]


del STs
del i
del k
del rep
del t
del temp
del Penha
del n
