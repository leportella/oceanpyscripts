# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 13:59:29 2015

@author: leportella
"""

import netCDF4 as nc
import numpy as np
from math import pi, radians, sin
import romslab as rl

def GetVariables(filenc):
    """
    Function to get all variables from a nectdf file into a dictionary.

    Examples:
        import netCDF4
        file = netCDF4.Dataset('file.nc')
        out = ncwork.GetVariables(file) """
        
    #sanity check
    if type(filenc) != nc._netCDF4.Dataset: 
        print 'The file is not in the right format'
    else: 
        listt = []
        for v in filenc.variables: listt.append(v)
    
        varr={}
        for tt in listt: 
          varr[tt]=filenc.variables[tt][:]
        return varr
    
    
def CalculateCoriolis(y_rho):
    """
    Helpful for ROMS grids
    Calculate Coriolis Acceleration in rho points. As Coriolis only uses latitude
    the input must be the y_rho variable
        out = CalculateCoriolis(y_rho)
        out is an array with same size as y_rho
    """
    f=np.zeros(shape=(len(y_rho),len(y_rho[0])))
    for yy in range(0,len(y_rho)):
        for xx in range(0,len(y_rho[yy])):
            if y_rho[yy][xx] > -999:
                f[yy][xx] = 2*(7.2921*10**-5)*sin(radians(y_rho[yy][xx]))
    return f


def rgfgrid2ROMS(filenc):
    """
    Gets a nc grid file generated by RGFRIG    
    
    """
        
    #sanity check
    if type(filenc) != nc._netCDF4.Dataset: 
        print 'The file is not in the right format'
    else:
        grd = GetVariables(filenc)
        ng={}
        ng['lon_rho'] = grd['lon_rho'][1:-2,1:-2]
        ng['lat_rho'] = grd['lat_rho'][1:-2,1:-2]
        ng['lon_psi'] = grd['lon_psi'][1:-2,1:-2]
        ng['lat_psi'] = grd['lat_psi'][1:-2,1:-2]
        ng['lon_u'] = grd['lon_u'][1:-2,1:-2]
        ng['lat_u'] = grd['lat_u'][1:-2,1:-2]
        ng['lon_v'] = grd['lon_v'][1:-2,1:-2]
        ng['lat_v'] = grd['lat_v'][1:-2,1:-2]
        ng['h'] = -grd['h'][1:-2,1:-2]        
        
        ng['pm'],ng['pn'],ng['dndx'],ng['dmde']=rl.get_metrics(ng['lat_u'],ng['lon_u'],ng['lat_v'],ng['lon_v'])
        ng['f']= CalculateCoriolis(ng['lat_rho'])
      
        bat = ng['h']
        mask=np.zeros([len(bat),len(bat[0])])
        for i in range(len(bat)):
            for j in range(len(bat[i])):
                if bat[i,j]>0: mask[i,j]=1
        
        u = ng['lon_u']
        masku=np.zeros([len(u),len(u[0])])
        for i in range(len(u)):
            for j in range(len(u[i])):
                if mask[i,j]==1: masku[i,j]=1
                    
        v = ng['lon_v']
        maskv=np.zeros([len(v),len(v[0])])
        for i in range(len(v)):
            for j in range(len(v[i])):       
                if mask[i,j]==1: maskv[i,j]=1:
                    
        p = ng['lon_psi']
        maskp=np.zeros([len(p),len(p[0])])
        for i in range(len(p)):
            for j in range(len(p[i])):     
                if mask[i,j]==0 or mask[i+1,j]==0: maskp[i,j]=0
                else: maskp[i,j]=1        
                
        ng['mark_rho'] = mask
        ng['mark_psi'] = maskp
        ng['mark_u'] = masku
        ng['mark_v'] = maskv
        
        
        print 'eta rho = ' + str(len(ng['lon_rho']))
        print 'xsi rho = ' + str(len(ng['lon_rho'][0]))
        print 'eta psi = ' + str(len(ng['lon_psi']))
        print 'xsi psi = ' + str(len(ng['lon_psi'][0]))
        print 'eta u = ' + str(len(ng['lon_u']))
        print 'xsi u = ' + str(len(ng['lon_u'][0]))
        print 'eta v = ' + str(len(ng['lon_v']))
        print 'xsi v = ' + str(len(ng['lon_v'][0]))
        
        return ng
        
def InsertGridDimensions(filenc,dirin):
    """
    """
    
    #sanity check
    if type(filenc) != nc._netCDF4.Dataset: 
        print 'The file is not in the right format'
    else:
        filenc.variables['lon_rho'][:] = dirin['lon_rho'][:]
        filenc.variables['lat_rho'][:] = dirin['lat_rho'][:]
        filenc.variables['lon_psi'][:] = dirin['lon_psi'][:]
        filenc.variables['lat_psi'][:] = dirin['lat_psi'][:]
        filenc.variables['lon_u'][:] = dirin['lon_u'][:]
        filenc.variables['lat_u'][:] = dirin['lat_u'][:]
        filenc.variables['lon_v'][:] = dirin['lon_v'][:]
        filenc.variables['lat_v'][:] = dirin['lat_v'][:]
        filenc.variables['dmde'][:] = dirin['dmde'][:]
        filenc.variables['dndx'][:] = dirin['dndx'][:]
        filenc.variables['pm'][:] = dirin['pm'][:]
        filenc.variables['pn'][:] = dirin['pn'][:]        
        filenc.variables['f'][:] = dirin['f'][:]  
        filenc.variables['h'][:] = dirin['h'][:] 
        filenc.variables['mask_rho'][:]=dirin['mark_rho'][:]
        filenc.variables['mask_psi'][:]=dirin['mark_psi'][:]
        filenc.variables['mask_u'][:]=dirin['mark_u'][:]
        filenc.variables['mask_v'][:]=dirin['mark_v'][:]
        
    return 'ok'