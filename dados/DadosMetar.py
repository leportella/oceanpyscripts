# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 13:47:55 2016

@author: leportella
"""

import sys

sys.path.insert(0,'/home/leportella/scripts/py/my/oceanpy/tools')

import csv
import numpy as np
from generaltools import *
import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pyproj import Proj
import datetime
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

met['vel'] = np.multiply(met['vel'], 0.5144)

temp = met['tempo']
dup = temp.duplicated()

met['vel'] = met['vel'][dup==False]
met['dir'] = met['dir'][dup==False]
met['tempo'] = met['tempo'][dup==False]

a = np.isnan(met['vel'])
b=np.logical_not(a)
temp = np.zeros(len(met['tempo'][a]))
vel_interp = met['vel'].interpolate()





plt.figure(figsize=(15,5))
plt.plot(met['tempo'], met['vel'])
plt.title(u'Velocidade do Vento - METAR')
plt.ylabel(u'Velocidade (m/s)')
#plt.xlim(met['tempo'][0], met['tempo'][-1])
plt.grid()
plt.savefig(dirOut + 'Vento_METAR_2011vel.png',dpi=200)


plt.figure(figsize=(15,5))
plt.plot(met['tempo'][b], met['vel'][b],'b')
plt.plot(met['tempo'][a].values, vel_interp[a],'.r')
plt.xlabel(u'Tempo')
plt.ylabel(u'Velocidade (m/s)')
plt.grid()
plt.legend([u'Dados Válidos', u'Dados Indisponíveis'],numpoints=1)
plt.title(u'Velocidade do Vento - Aeroporto de Navegantes')
plt.savefig(dirOut + 'Vento_Metar_Nans.png',dpi=200)

################# WINDROSE METAR (TODOS OS DADOS) ################################
plotaWindRose(met['dir'],met['vel'],maxYlabel=30, maxLeg=9, stepLeg=2)  
plt.savefig(dirOut + 'Vento_Metar_2011_Windrose.png',dpi=200)


################## PLOT VEL VENTO METAR (TODOS OS DADOS) ########################
plt.figure(figsize=(15,5))
plt.plot(met['tempo'],met['vel'])
plt.title(u'Velocidade do Vento - Aeroporto de Navegantes')
plt.ylabel(u'Velocidade (m/s)')
plt.grid()
plt.savefig(dirOut + 'Vento_Metar_2011_vel.png',dpi=200)


################# HISTOGRAMA VEL VENTO METAR (todos os dados) ###################
PercentHistogram(met['vel'],binss=50)
plt.title(u'Histograma de Velocidade do Vento - Aeroporto de Navegantes')
plt.ylabel(u'Percentual')
plt.xlabel(u'Velocidade (m/s)')
plt.xlim(0,10)
plt.grid()
plt.savefig(dirOut + 'Vento_Metar_2011_histvel.png',dpi=200)

################# HISTOGRAMA DIR VENTO METAR (todos os dados) ###################
PercentHistogram(met['dir'],binss=50)
plt.title(u'Histograma de Direção do Vento - Aeroporto de Navegantes')
plt.ylabel(u'Percentual')
plt.xlabel(u'Velocidade (m/s)')
plt.xlim(0,360)
plt.grid()
plt.savefig(dirOut + 'Vento_Metar_2011_histdir.png',dpi=200)


latmin=-27.2
latmax=-26
lonmin=-49
lonmax=-48

m = Basemap(projection='cyl', resolution='f', llcrnrlon=lonmin, llcrnrlat=latmin , urcrnrlon=lonmax , urcrnrlat=latmax )
fig = plt.figure()
m.drawcoastlines(linewidth=0.25,color = 'k')
m.fillcontinents(color='0.8',lake_color='aqua')
m.plot(-48.651,-26.8833, 'b.', markersize=10,label='Selecionado')
plt.title(u'METAR - Estação SBNF',fontsize=12)
#plt.legend([u'Disponível',u'Selecionado'],numpoints=1)
m.drawparallels(np.arange(latmin,latmax,0.5),labels=[1,0,0,0])
m.drawmeridians(np.arange(lonmin,lonmax,0.5),labels=[0,0,0,1])
plt.savefig(dirOut + 'METAR_position.png',dpi=200)