#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys

sys.path.insert(0,'/home/leportella/scripts/pyscripts/myscripts/open')
sys.path.insert(0,'/home/leportella/scripts/pyscripts/ttide_py-master/ttide')

import csv
import numpy as np
from generaltools import *
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy.fft as fft
from ttide.t_tide import t_tide
from windrose import WindroseAxes

direct = '/home/leportella/Documents/master/dados/utilizacao/'
dirOut = '/home/leportella/Documents/master/dissertacao/ProjetoLatex/dis_controlada/figuras/'

#################################################################################
##                                                                             ##
##                       DADOS DE PIÇARRAS                                     ##
##                                                                             ##
#################################################################################

ST001=np.array(list(csv.reader(open(direct+'ST001_Nivel_Temp.csv','rb'),delimiter=';'))[1:],dtype=np.float64)
ST002=np.array(list(csv.reader(open(direct+'ST002_Nivel_Temp.csv','rb'),delimiter=','))[1:],dtype=np.float64)
ST003=np.array(list(csv.reader(open(direct+'ST003_Nivel_Temp.csv','rb'),delimiter=','))[1:],dtype=np.float64)

STs = {1: ST001, 2: ST002, 3: ST003}
sts = {k: None for k in range(1, 4)}

for k in range(1,4): #loop pros 3 pontos
    t=[]
    rep = STs[k]
    
    for i in range(0,len(rep)): #loop pra fazer o datenum (vetor tempo)
        t.append(
            datetime.datetime(
                int(rep[i,0]), int(rep[i,1]), int(rep[i,2]),
                int(rep[i,3]), int(rep[i,4]), int(rep[i,5])
            )
        )
  
    if k==3:
        temp=np.subtract(t,datetime.timedelta(hours=3))
        t2 = pd.Series(temp)
        sts[k] = {'tempo': t2}
    else:
        t = pd.Series(t)
        sts[k] = {'tempo': t}
    
    sts[k]['nivel'] = pd.Series(rep[:,6])
    sts[k]['temp'] = pd.Series(rep[:,7])
    
    sts[k]['nivel'][sts[k]['nivel']==999]=np.nan
    sts[k]['temp'][sts[k]['temp']==999]=np.nan
    
    sts[k]['nivelinterp']=sts[k]['nivel'].interpolate()
    sts[k]['tempinterp']=sts[k]['temp'].interpolate()
    
    sts[k]['media_nivel']=np.mean(sts[k]['nivel'])
    sts[k]['mediana_nivel']=np.median(sts[k]['nivel'])
    sts[k]['max_nivel']=np.max(sts[k]['nivel'])    
    sts[k]['min_nivel']=np.min(sts[k]['nivel'])
    sts[k]['std_nivel']=np.std(sts[k]['nivel'])
    

    sts[k]['media_temp']=np.mean(sts[k]['temp'])
    sts[k]['mediana_temp']=np.median(sts[k]['temp'])
    sts[k]['max_temp']=np.max(sts[k]['temp'])    
    sts[k]['min_temp']=np.min(sts[k]['temp'])
    sts[k]['std_temp']=np.std(sts[k]['temp'])
    
    sts[k]['spectrum']=fft.fft(sts[k]['nivelinterp'][0::2])
    sts[k]['freq'] = fft.fftfreq(len(sts[k]['spectrum']))    
    
    sts[k]['nameu1'], sts[k]['fu1'], sts[k]['tideconout1'], sts[k]['xout1'] = t_tide((sts[k]['nivelinterp']-sts[k]['media_nivel'])*100, dt=0.5, lat=np.array(-25))

    sts[k]['previsaottide'] = sts[k]['xout1'].squeeze()/100    
    
#    plt.figure(figsize=(15,5))
#    plt.plot(sts[k]['tempo'],sts[k]['nivel'],)
#    plt.title(u'Nível - ST00' + str(k))
#    plt.ylabel(u'Nível (m)')
#    plt.grid()
#    plt.savefig(dirOut + 'Nivel_ST00' + str(k) + '.png',dpi=200)

#################################################################################
##                                                                             ##
##                  PLOT FIGURAS DE NIVEL DE PIÇARRAS                          ##
##                                                                             ##
#################################################################################    


######################## fft com eixo em log ####################################
#plt.figure(figsize=(15,5))
#plt.semilogx(sts[1]['freq'], sts[1]['spectrum'])
#plt.semilogx(sts[2]['freq'], sts[2]['spectrum'],'r')
#plt.semilogx(sts[3]['freq'], sts[3]['spectrum'],'g')
#plt.xlim(0.001,0.2)
#plt.ylim(0,100)
#plt.xlabel(u'Frequência')
#plt.grid()
#plt.legend(['ST001', 'ST002','ST003'])
#plt.title(u'Espectro da Maré - Piçarras 2011')
#plt.savefig(dirOut + 'Espectro_FFT_Picarras_Logx.png',dpi=200)

######################## fft com eixo x normal###################################
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

######################## nivel medido e previsto#################################

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
##                  PLOT FIGURAS DE NIVEL DE PENHA                             ##
##                                                                             ##
#################################################################################    


Penha=np.array(list(csv.reader(open(direct+'maregrafo_penha.csv','rb'),delimiter=',')),dtype=np.float64)

t=[]
for i in range(0,len(Penha)):
    t.append(datetime.datetime(int(Penha[i,2]),int(Penha[i,1]),int(Penha[i,0]),int(Penha[i,3]),int(Penha[i,4]),int(Penha[i,5])))

penha={'tempo':pd.Series(t)}
penha['nivel']=pd.Series(Penha[:,6]/100)


penha['spectrum']=abs(fft.fft(penha['nivel']))
penha['freq'] = fft.fftfreq(len(penha['spectrum']))

#plt.figure(figsize=(15,5))
#plt.plot(penha['tempo'],penha['nivel'])
#plt.title(u'Nível - Penha')
#plt.ylabel(u'Nível (m)')
#plt.grid()
#plt.savefig(dirOut + 'Nivel_Penha.png',dpi=200)
#
#plt.figure(figsize=(15,5))
#plt.semilogx(penha['freq'], penha['spectrum'])
#plt.xlim(0,0.5)
#plt.xlabel(u'Frequência')
#plt.grid()
#plt.title(u'Espectro da Maré - Penha 95-96')
#plt.savefig(dirOut + 'Espectro_FFT_Penha_Logx.png',dpi=200)
#

#################################################################################
##                                                                             ##
##                  PLOT FIGURAS DE TEMP DE PENHA                              ##
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

#################################################################################
##                                                                             ##
##                  DADOS DE VENTO                                             ##
##                                                                             ##
#################################################################################   


#!!!!!!!!!!!!CONFERIR

#metar=np.array(list(csv.reader(open(direct+'metar_01-01-2011_31-12-2011.csv','rb'),delimiter=','))[1:],dtype=np.float64)
#
#t=[]
#for i in range(0,len(metar)):
#    t.append(datetime.datetime(int(metar[i,2]),int(metar[i,1]),int(metar[i,0]),int(metar[i,3]),int(metar[i,4]),0))
#
#met={'tempo':pd.Series(t)}
#
#met['dir']=pd.Series(metar[:,5])
#met['vel']=pd.Series(metar[:,6])
#
#ax = WindroseAxes.from_ax()
#ax.bar(met['dir'],met['vel'], normed=True, edgecolor='white')
#ax.set_legend()
##ax.legend(bbox_to_anchor=(0.9, 0.9))
#l = ax.legend(axespad=-0.10)
#plt.setp(l.get_texts(), fontsize=8)
#ax.set_yticks(range(0, 30, 5))  
#ax.set_yticklabels(map(str, range(0, 30, 5)))
#plt.savefig(dirOut + 'WindRose_Metar_2011.png',dpi=200)




