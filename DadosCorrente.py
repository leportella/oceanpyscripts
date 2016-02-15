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
    
 
    sts[k]['umean'] = series[us][0:-1].mean(axis=1)
    sts[k]['vmean'] = series[vs][0:-1].mean(axis=1)
     
    out2 = uv2veldir(sts[k]['umean'], sts[k]['vmean'])
     
    sts[k]['velmean'] = out2['vel']
    sts[k]['dirmean'] = out2['dir']   
     
############################# PLOT WINDROSE #####################################

    plotaWindRose(sts[k]['dirmean'],sts[k]['velmean'],maxYlabel=40, maxLeg=0.30, stepLeg=0.1)     
    plt.savefig(dirOut + 'CurrentRose_ST00' + str(k) + '_DepthAv.png',dpi=200)
    
    