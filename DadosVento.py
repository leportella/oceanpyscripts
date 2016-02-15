# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 13:47:55 2016

@author: leportella
"""

import sys

sys.path.insert(0,'/home/leportella/scripts/pyscripts/myscripts/open')

import csv
import numpy as np
from generaltools import *
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from windrose import WindroseAxes

direct = '/home/leportella/Documents/master/dados/utilizacao/'
dirOut = '/home/leportella/Documents/master/dissertacao/Latex/dis_controlada/figuras/'

#################################################################################
##                                                                             ##
##                  DADOS DE VENTO METAR                                       ##
##                                                                             ##
#################################################################################   

metar=np.array(list(csv.reader(open(direct+'metar_01-01-2011_31-12-2011.csv','rb'),delimiter=','))[1:],dtype=np.float64)

t=[]
for i in range(0,len(metar)):
    t.append(datetime.datetime(int(metar[i,2]),int(metar[i,1]),int(metar[i,0]),int(metar[i,3]),int(metar[i,4]),0))

met={'tempo':pd.Series(t)}

met['dir']=pd.Series(metar[:,5])
met['vel']=pd.Series(metar[:,6])


################# WINDROSE METAR (TODOS OS DADOS) ################################
plotaWindRose(met['dir'],met['vel'],maxvalue=30)
plt.savefig(dirOut + 'Metar_2011_Windrose_total.png',dpi=200)

################### WINDROSE METAR (abaixo de 20) ################################
#
#
#
#fig = plt.figure(figsize=(20,20),facecolor='w', edgecolor='w')
#ax = WindroseAxes.from_ax(fig=fig)
#ax.bar(met['dir'],met['vel'], normed=True, edgecolor='white')
#ax.set_legend()
#ax.legend(bbox_to_anchor=(1.1, 0.4))
#ax.set_yticks(range(0, 30, 5))  
#ax.set_yticklabels(map(str, range(0, 30, 5)))
#plt.savefig(dirOut + 'Metar_2011_Windrose_ate20.png',dpi=300)

################## PLOT VEL VENTO METAR (TODOS OS DADOS) ########################
plt.figure(figsize=(15,5))
plt.plot(met['tempo'],met['vel'])
plt.title(u'Velocidade do Vento - Aeroporto de Navegantes')
plt.ylabel(u'Velocidade (m/s)')
plt.grid()
plt.savefig(dirOut + 'Metar_2011_veltotal.png',dpi=200)

################## PLOT VEL VENTO METAR (ABAIXO DE 20) ##########################
plt.figure(figsize=(15,5))
plt.plot(met['tempo'][met['vel']<20],met['vel'][met['vel']<20])
plt.title(u'Velocidade do Vento - Aeroporto de Navegantes')
plt.ylabel(u'Velocidade (m/s)')
plt.grid()
plt.savefig(dirOut + 'Metar_2011_vel_abaixo20.png',dpi=200)

################# HISTOGRAMA VEL VENTO METAR (todos os dados) ###################
PercentHistogram(met['vel'],binss=30)
plt.title(u'Histograma de Velocidade do Vento - Aeroporto de Navegantes')
plt.ylabel(u'Percentual')
plt.xlabel(u'Velocidade (m/s)')
plt.grid()
plt.savefig(dirOut + 'Metar_2011_histvel_total.png',dpi=200)

################### HISTOGRAMA VEL VENTO METAR (abaixo de 20) ###################
PercentHistogram(met['vel'][met['vel']<20],binss=30)
plt.title(u'Histograma de Velocidade do Vento - Aeroporto de Navegantes')
plt.ylabel(u'Percentual')
plt.xlabel(u'Velocidade (m/s)')
plt.grid()
plt.savefig(dirOut + 'Metar_2011_histvel_abaixo20.png',dpi=200)

#################################################################################
##                                                                             ##
##                  DADOS DE VENTO CFSR                                        ##
##                                                                             ##
#################################################################################   

cf=np.loadtxt(direct+'VENTO_CFSR_7-1-1999_2-1-2015_1.txt')
t=[]
for i in range(0,len(cf)):
    t.append(datetime.datetime(int(cf[i,0]),int(cf[i,1]),int(cf[i,2]),int(cf[i,3]),0,0))

cfsr=uv2veldir(cf[:,4],cf[:,5])
cfsr['tempo']=pd.Series(t)


#inicio 2009=10309
#inicio 2011=13228

#
################## WINDROSE CFSR (TODOS OS DADOS) ##############################

    
plotaWindRose(cfsr['dir'],cfsr['vel'],maxvalue=20,intervalo=5)
plt.savefig(dirOut + 'CFSR_1999-2015_Windrose_total.png',dpi=200)


################### PLOT VEL VENTO CFSR (TODOS OS DADOS) ########################
#plt.figure(figsize=(15,5))
#plt.plot(cfsr['tempo'],cfsr['vel'])
#plt.title(u'Velocidade do Vento -  CFSR')
#plt.ylabel(u'Velocidade (m/s)')
#plt.grid()
#plt.savefig(dirOut + 'CFSR_1999-2015_veltotal.png',dpi=200)
#
################## HISTOGRAMA VEL VENTO CFSR (todos os dados) ###################
#PercentHistogram(cfsr['vel'],binss=30)
#plt.title(u'Histograma de Velocidade do Vento - CFSR')
#plt.ylabel(u'Percentual')
#plt.xlabel(u'Velocidade (m/s)')
#plt.grid()
#plt.savefig(dirOut + 'CFSR_1999-2015_histvel_total.png',dpi=200)


ts=10309 #inicio de 2009

##################### WINDROSE CFSR (2009-2015) #################################

plotaWindRose(cfsr['dir'][ts:-1],cfsr['vel'][ts:-1],maxvalue=20)
plt.savefig(dirOut + 'CFSR_2009-2015_Windrose_total.png',dpi=300)

################## PLOT VEL VENTO CFSR (2009-2015)  #############################
plt.figure(figsize=(15,5))
plt.plot(cfsr['tempo'][ts:-1].values,cfsr['vel'][ts:-1].values)
plt.title(u'Velocidade do Vento -  CFSR')
plt.ylabel(u'Velocidade (m/s)')
plt.grid()
plt.savefig(dirOut + 'CFSR_2009-2015_veltotal.png',dpi=200)

################# HISTOGRAMA VEL VENTO CFSR (2009-2015)  ########################
PercentHistogram(cfsr['vel'][ts:-1].values,binss=30)
plt.title(u'Histograma de Velocidade do Vento - CFSR')
plt.ylabel(u'Percentual')
plt.xlabel(u'Velocidade (m/s)')
plt.grid()
plt.savefig(dirOut + 'CFSR_2009-2015_histvel_total.png',dpi=200)

