# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 20:43:15 2016

@author: leportella
"""

import sys
sys.path.insert(0,'/home/leportella/scripts/py/my/oceanpy/tools/')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

WD = '/home/leportella/Documents/master/'
directory = '{}dados/utilizacao/'.format(WD)
outputDirectory = '{}dissertacao/Latex/dis_controlada/figuras/english'.format(WD)

structure = ['Year',	'Month', 'Day', 'Hour', 'Minute', 
             'Hm0', 'H10', 'Hmax', 'DirTp', 'SprTp', 
             'MeanDir', 'Tp', 'Tm02']
              
# Read CSV
ST001 = pd.read_csv(directory+'ST001_Wave.csv')              
ST002 = pd.read_csv(directory+'ST002_Wave.csv')      
ST003 = pd.read_csv(directory+'ST003_Wave.csv')      
              
STs = {1: ST001, 2: ST002, 3: ST003}
sts = {k: None for k in range(1, 4)}

for k in range(1,4): #loop pros 3 pontos
    tempo = []
    dado = STs[k]
    
    for i in range(0,len(dado)): #loop pra fazer o datenum (vetor tempo)
        tempo.append(datetime(
                    int(dado['Year'][i]), int(dado['Month'][i]), int(dado['Day'][i]),
                    int(dado['Hour'][i]), int(dado['Minute'][i]), 0))
  
    if k==3:
        tempolocal = np.subtract(tempo, timedelta(hours=3))
        sts[k] = {'tempo': tempolocal}
    else:
        sts[k] = {'tempo': tempo}
    
    sts[k]['Hm0'] = pd.Series(STs[k]['Hm0'])
    sts[k]['Tp'] = pd.Series(STs[k]['Tp'])
    sts[k]['MeanDir'] = pd.Series(STs[k]['MeanDir'])
        
    sts[k]['Hm0'][sts[k]['Hm0']>900]=np.nan
    sts[k]['Tp'][sts[k]['Tp']>900]=np.nan
    sts[k]['MeanDir'][sts[k]['MeanDir']>900]=np.nan
    
    Hm0 = sts[k]['Hm0']
    Tp = sts[k]['Tp']
    MeanDir = sts[k]['MeanDir']
    
    sts[k]['Hm0'] = Hm0.interpolate()
    sts[k]['Tp'] = Tp.interpolate()
    sts[k]['MeanDir'] = MeanDir.interpolate()


plt.figure(figsize=(15,5))
plt.plot(sts[1]['tempo'], sts[1]['Hm0'],':')
plt.plot(sts[2]['tempo'], sts[2]['Hm0'],'r')
plt.plot(sts[3]['tempo'], sts[3]['Hm0'],'--g')
plt.title(u'Significant Wave Height (Hm0)')
plt.ylabel(u'Hm0 (m)')
plt.legend(['ST001', 'ST002','ST003'])
plt.grid()
plt.savefig(outputDirectory + 'Significant_Wave_Height.png',dpi=200)

plt.figure(figsize=(15,5))
plt.plot(sts[1]['tempo'], sts[1]['Tp'],'o')
plt.plot(sts[2]['tempo'], sts[2]['Tp'],'^r')
plt.plot(sts[3]['tempo'], sts[3]['Tp'],'sg')
plt.title(u'Peak Period (Tp)')
plt.ylabel(u'Tp (s)')
plt.grid()
plt.legend(['ST001', 'ST002','ST003'])
plt.savefig(outputDirectory + 'PeakPeriod.png',dpi=200)

plt.figure(figsize=(15,5))
plt.plot(sts[1]['tempo'], sts[1]['MeanDir'],'o')
plt.plot(sts[2]['tempo'], sts[2]['MeanDir'],'^r')
plt.plot(sts[3]['tempo'], sts[3]['MeanDir'],'sg')
plt.title(u'Mean Direction (MeanDir)')
plt.ylabel(u'Mean Direction (Degrees)')
plt.grid()
plt.legend(['ST001', 'ST002','ST003'])
plt.savefig(outputDirectory + 'MeanDirection.png',dpi=200)

