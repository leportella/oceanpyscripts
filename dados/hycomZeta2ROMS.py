# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import netCDF4 as nc
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import numpy.ma as ma
import shutil

#grid do modelo 
grd=nc.Dataset(r'Y:\grid_v1_roms.nc')
lonr = grd.variables['lon_rho'][:][1:-2,1:-2]
latr = grd.variables['lat_rho'][:][1:-2,1:-2]

#plt.plot(lonr[0],latr[0],'.k') #fronteira sul
#plt.plot(lonr[-1],latr[-1],'.k') #fronteira norte
#
#plt.plot(lonr[:,0],latr[:,0],'.k') #fronteira oeste
#plt.plot(lonr[:,-1],latr[:,-1],'.k') #fronteira leste



#copy bry_unlimit
shutil.copy2(r'Y:\bry_unlimit.nc',r'Y:\bryfiles\sulbrasil_bry_v01.nc') 
bry=nc.Dataset(r'Y:\bryfiles\sulbrasil_bry_v01.nc','r+') 
    
for i in range(1,537):
    #dado do hycom de salinidade
    hy=nc.Dataset(r'Y:\hycom_data\Hycom_2012_t' + str(i).zfill(4)  +'_surfel.nc')
    hylat = hy.variables['lat'][:]
    hylon = hy.variables['lon'][:]
    hyzeta = hy.variables['surf_el'][0,:,:]
    hytime = hy.variables['time'][:]
    
    #definindo lon e lat na grade
    xy=np.meshgrid(hylon,hylat)
    
    #deixando as infos em 1 coluna apenas
    xgrd=np.reshape(lonr,(-1,1))
    ygrd=np.reshape(latr,(-1,1))
    
    x=np.reshape(xy[0],(-1,1))
    y=np.reshape(xy[1],(-1,1))
    z=np.reshape(hyzeta,(-1,1))
    
    #retirando os valores que estiverem contidos dentro da máscara dos dados do hycom
    out=np.logical_not(ma.getmask(z))
    x=x[out]
    y=y[out]
    z=z[out]
    
    #empilhando xy para a interpolação
    xy2=np.column_stack([x,y])
    
    #interpolação fronteira sul
    zetaS = griddata(xy2 , z, (lonr[0], latr[0]), method='linear')
    zetaN = griddata(xy2 , z, (lonr[-1], latr[-1]), method='linear')
    zetaE = griddata(xy2 , z, (lonr[:,-1], latr[:,-1]), method='linear')
    
     
    bry.variables['zeta_north'][i-1,:]=zetaN[:]
    bry.variables['zeta_south'][i-1,:]=zetaS[:]
    bry.variables['zeta_east'][i-1,:]=zetaE[:]
    bry.variables['bry_time'][i-1]=hytime[:]
    
    print str(i) + ' ok!'
#plt.scatter(lonr[0],latr[0],c=salS,edgecolors='none')
#plt.scatter(lonr[-1],latr[-1],c=salN,edgecolors='none')
#plt.scatter(lonr[:,-1],latr[:,-1],c=salE,edgecolors='none')

