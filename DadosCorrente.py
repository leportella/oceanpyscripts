#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Mon Feb 15 14:45:16 2016

@author: leportella
"""

import sys

sys.path.insert(0,'/home/leportella/scripts/pyscripts/myscripts/open')
sys.path.insert(0,'/home/leportella/scripts/pyscripts/ttide_py-master/ttide')

import csv
import numpy as np
from generaltools import *
import datetime
import matplotlib.pyplot as plt
import pandas as pd


direct = '/home/leportella/Documents/master/dados/utilizacao/'
dirOut = '/home/leportella/Documents/master/dissertacao/Latex/dis_controlada/figuras/'


#################################################################################
##                                                                             ##
##                       DADOS ADCPS PIÇARRAS                                  ##
##                                                                             ##
#################################################################################

ST001=np.array(list(csv.reader(open(direct+'ST001_Corrente.csv','rb'),delimiter=','))[1:],dtype=np.float64)
ST002=np.array(list(csv.reader(open(direct+'ST002_Corrente.csv','rb'),delimiter=','))[1:],dtype=np.float64)
ST003=np.array(list(csv.reader(open(direct+'ST003_Corrente.csv','rb'),delimiter=','))[1:],dtype=np.float64)

STs = {1: ST001, 2: ST002, 3: ST003}
sts = {k: None for k in range(1, 4)}

for k in range(1,4): #loop pros 3 pontos
    t=[]
    rep = STs[k]
    
    for i in range(0,len(rep)): #loop pra fazer o datenum (vetor tempo)
        t.append(
            datetime.datetime(
                int(rep[i,2]), int(rep[i,1]), int(rep[i,0]),
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
    
    
    lim = len(STs[k][0])
    numcels = (lim-6)/2
    c=1
    
    #sts[k]['numcels'] = numcels
    for n in range(6,lim-1,2):
        
        u = pd.Series(rep[:,n])
        v = pd.Series(rep[:,n+1])
        
        u[u>990]=np.nan
        v[v>990]=np.nan
        
        sts[k]['u%s' % c] = u.interpolate()
        sts[k]['v%s' % c] = v.interpolate()
          
        out = uv2veldir(sts[k]['u%s' % c], sts[k]['v%s' % c])
        
        sts[k]['vel%s' % c] = out['vel']
        sts[k]['dir%s' % c] = out['dir']
        
        c+=1

#################################################################################
##                                                                             ##
##                             DEPTH AVERAGE                                   ##
##                                                                             ##
#################################################################################

    series = pd.DataFrame(sts[k])
    us = [col for col in series if 'u' in col]
    vs = [col for col in series if 'v' in col]
 
    sts[k]['u_depthav'] = series[us][:].mean(axis=1)
    sts[k]['v_depthav'] = series[vs][:].mean(axis=1)
     
    out2 = uv2veldir(sts[k]['u_depthav'], sts[k]['v_depthav'])
     
    sts[k]['vel_depthav'] = out2['vel']
    sts[k]['dir_depthav'] = out2['dir']   
    sts[k]['vel_depthav_cm'] =  sts[k]['vel_depthav']*100
    
    uresidual_50h = []    
    vresidual_50h = []  
    
    for i in range(0,len(sts[k]['u_depthav'])-50,50):
        uresidual_50h.append(np.mean(sts[k]['u_depthav'][i:i+50]))
        vresidual_50h.append(np.mean(sts[k]['v_depthav'][i:i+50]))
    
    sts[k]['uresidual_50h']=uresidual_50h
    sts[k]['vresidual_50h']=vresidual_50h


#    ############################### QUIVER CORRENTE #####################################
#    fig, (ax0, ax1) = plt.subplots(nrows=2, sharey=False, sharex=False, figsize=(11, 5))
#    
#    q = ax0.quiver(sts[k]['u_depthav'],sts[k]['v_depthav'],scale=3)
#    p = plt.quiverkey(q,1480,0.05,0.1,"0.1 m/s",coordinates='data',color='k')
#    ax0.axes.get_yaxis().set_visible(False)
#    ax0.axes.get_xaxis().set_visible(False)
#    ax0.set_ylim(-0.02,0.08)
#    ax0.set_xlim(0,len(sts[k]['u_depthav']))
#    ax0.set_title('Vetores de Corrente - ST00' + str(k))
#    
#    ax1.plot(sts[k]['tempo'],sts[k]['vel_depthav'])
#    ax1.grid()
#    ax1.set_ylim(0,0.3)
#    ax1.set_title('Velocidade da Corrente - ST00' + str(k))
#    plt.savefig(dirOut + 'Corrente_Quiver_ST00' + str(k) + '.png',dpi=200)


################################ CORRENTE RESIDUAL #####################################
#fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, sharey=False, sharex=False, figsize=(11, 5))
#
#q = ax0.quiver(sts[1]['uresidual_50h'],sts[1]['vresidual_50h'],scale=0.8,width=0.005)
#p = plt.quiverkey(q,29,0.05,0.05,"0.05 m/s",coordinates='data',color='k')
#ax0.axes.get_yaxis().set_visible(False)
#ax0.axes.get_xaxis().set_visible(False)
#ax0.set_ylim(-0.02,0.08)
#ax0.set_xlim(0,len(sts[1]['uresidual_50h']))
#ax0.set_title('Corrente Residual - 50h - ST001',fontsize=12)
#
#q = ax1.quiver(sts[2]['uresidual_50h'],sts[2]['vresidual_50h'],scale=0.8,width=0.005)
#p = plt.quiverkey(q,29,0.05,0.05,"0.05 m/s",coordinates='data',color='k')
#ax1.axes.get_yaxis().set_visible(False)
#ax1.axes.get_xaxis().set_visible(False)
#ax1.set_ylim(-0.02,0.08)
#ax1.set_xlim(0,len(sts[2]['uresidual_50h']))
#ax1.set_title('Corrente Residual - 50h - ST002',fontsize=12)
#
#q = ax2.quiver(sts[3]['uresidual_50h'],sts[3]['vresidual_50h'],scale=0.8,width=0.005)
#p = plt.quiverkey(q,29,0.05,0.05,"0.05 m/s",coordinates='data',color='k')
#ax2.axes.get_yaxis().set_visible(False)
#ax2.axes.get_xaxis().set_visible(True)
#ax2.set_ylim(-0.02,0.08)
#ax2.set_xlim(0,len(sts[3]['uresidual_50h']))
#ax2.set_title('Corrente Residual - 50h - ST003',fontsize=12)
#
#labels = [item.get_text() for item in ax2.get_xticklabels()]
#labels[0] = '0 h'
#labels[1] = '250 h'
#labels[2] = '500 h'
#labels[3] = '750 h'
#labels[4] = '1000 h'
#labels[5] = '1250 h'
#labels[6] = '1500 h'
#
#ax2.set_xticklabels(labels)
#plt.savefig(dirOut + 'Corrente_Residual_Medida_50h.png',dpi=200)



############################### PLOT WINDROSE ###############################

#    plotaWindRose(sts[k]['dir_depthav'],sts[k]['vel_depthav'],maxYlabel=40, maxLeg=0.30, stepLeg=0.1)     
#    plt.savefig(dirOut + 'CurrentRose_ST00' + str(k) + '_DepthAv.png',dpi=200)
#    
#    plotaWindRose(sts[k]['dir_depthav'],sts[k]['vel_depthav_cm'],maxYlabel=40, maxLeg=30, stepLeg=5)     
#    plt.savefig(dirOut + 'CurrentRose_ST00' + str(k) + '_DepthAv_CM.png',dpi=200)    
    
############################## PLOT HISTOGRAMA ###################################
#    PercentHistogram(sts[k]['vel_depthav'],binss=30)
#    plt.title(u'Histograma de Velocidade da Corrente Medida - ST00' + str(k))
#    plt.ylabel(u'Percentual')
#    plt.xlabel(u'Velocidade (m/s)')
#    plt.grid()
#    plt.savefig(dirOut + 'Corrente_ST00' + str(k) + '_HistVento.png',dpi=200)
#    
#    PercentHistogram(sts[k]['dir_depthav'],binss=30)
#    plt.title(u'Histograma de Direção da Corrente Medida - ST00' + str(k))
#    plt.ylabel(u'Percentual')
#    plt.xlabel(u'Graus')
#    plt.grid()
#    plt.savefig(dirOut + 'Corrente_ST00' + str(k) + '_HistDirecao.png',dpi=200)
#
#    plt.figure()
#    plt.plot(sts[k]['tempo'],sts[k]['vel_depthav'])
#    plt.title(u'Velocidade da Corrente Medida - ST00' + str(k))
#    plt.ylabel(u'Velocidade (m/s)')
#    plt.grid()
#    plt.savefig(dirOut + 'Corrente_ST00' + str(k) + '_Velocidade.png',dpi=200)
#    
    
#################################################################################
##                                                                             ##
##                              COMPARACAO COM VENTO                           ##
##                                                                             ##
#################################################################################

plt.figure(figsize=(15,5))
plt.plot(cfsr['tempo'],cfsr['vel'],'r')
ax = plt.gca()
ax2 = ax.twinx()
ax2.plot(sts[1]['tempo'],sts[1]['vel_depthav'],'b')
plt.xlim(sts[1]['tempo'][1],sts[1]['tempo'][len(sts[1]['tempo'])-1])
ax2.set_ylim(0,0.3)
plt.title(u'Velocidade da Corrente em ST001 e Velocidade do Vento')
ax.set_ylabel(u'Velocidade do Vento (m/s)',color='red')
ax2.set_ylabel(u'Velocidade da Corrente (m/s)',color='blue')
plt.grid()
plt.savefig(dirOut + 'Corrente_Vento_ST001.png',dpi=200)

plt.figure(figsize=(15,5))
plt.plot(cfsr['tempo'],cfsr['vel'],'r')
ax = plt.gca()
ax2 = ax.twinx()
ax2.plot(sts[2]['tempo'],sts[2]['vel_depthav'],'b')
plt.xlim(sts[2]['tempo'][1],sts[2]['tempo'][len(sts[2]['tempo'])-1])
ax2.set_ylim(0,0.3)
plt.title(u'Velocidade da Corrente em ST002 e Velocidade do Vento')
ax.set_ylabel(u'Velocidade do Vento (m/s)',color='red')
ax2.set_ylabel(u'Velocidade da Corrente (m/s)',color='blue')
plt.grid()
plt.savefig(dirOut + 'Corrente_Vento_ST002.png',dpi=200)

plt.figure(figsize=(15,5))
plt.plot(cfsr['tempo'],cfsr['vel'],'r')
ax = plt.gca()
ax2 = ax.twinx()
ax2.plot(sts[3]['tempo'],sts[3]['vel_depthav'],'b')
plt.xlim(sts[3]['tempo'][1],sts[3]['tempo'][len(sts[1]['tempo'])-1])
ax2.set_ylim(0,0.3)
plt.title(u'Velocidade da Corrente em ST003 e Velocidade do Vento')
ax.set_ylabel(u'Velocidade do Vento (m/s)',color='red')
ax2.set_ylabel(u'Velocidade da Corrente (m/s)',color='blue')
plt.grid()
plt.savefig(dirOut + 'Corrente_Vento_ST003.png',dpi=200)



###################
plt.figure(figsize=(15,5))
plt.plot(cfsr['tempo'],cfsr['dir'],'r')
ax = plt.gca()
ax2 = ax.twinx()
ax2.plot(sts[1]['tempo'],sts[1]['vel_depthav'],'b')
plt.xlim(sts[1]['tempo'][1],sts[1]['tempo'][len(sts[1]['tempo'])-1])
ax2.set_ylim(0,0.3)
plt.title(u'Velocidade da Corrente em ST001 e Direção do Vento')
ax.set_ylabel(u'Direção do Vento (graus)',color='red')
ax2.set_ylabel(u'Velocidade da Corrente (m/s)',color='blue')
plt.grid()
plt.savefig(dirOut + 'Corrente_VentoDir_ST001.png',dpi=200)

plt.figure(figsize=(15,5))
plt.plot(cfsr['tempo'],cfsr['dir'],'r')
ax = plt.gca()
ax2 = ax.twinx()
ax2.plot(sts[2]['tempo'],sts[2]['vel_depthav'],'b')
plt.xlim(sts[2]['tempo'][1],sts[2]['tempo'][len(sts[2]['tempo'])-1])
ax2.set_ylim(0,0.3)
plt.title(u'Velocidade da Corrente em ST002 e Velocidade do Vento')
ax.set_ylabel(u'Direção do Vento (graus)',color='red')
ax2.set_ylabel(u'Velocidade da Corrente (m/s)',color='blue')
plt.grid()
plt.savefig(dirOut + 'Corrente_VentoDir_ST002.png',dpi=200)

plt.figure(figsize=(15,5))
plt.plot(cfsr['tempo'],cfsr['dir'],'r')
ax = plt.gca()
ax2 = ax.twinx()
ax2.plot(sts[3]['tempo'],sts[3]['vel_depthav'],'b')
plt.xlim(sts[3]['tempo'][1],sts[3]['tempo'][len(sts[1]['tempo'])-1])
ax2.set_ylim(0,0.3)
plt.title(u'Velocidade da Corrente em ST003 e Velocidade do Vento')
ax.set_ylabel(u'Direção do Vento (graus)',color='red')
ax2.set_ylabel(u'Velocidade da Corrente (m/s)',color='blue')
plt.grid()
plt.savefig(dirOut + 'Corrente_VentoDir_ST003.png',dpi=200)