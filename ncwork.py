# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 13:59:29 2015

@author: leportella
"""

import netCDF4 as nc
import numpy as np
from math import pi, radians, sin

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
       
    listt = []
    for v in filenc.variables: listt.append(v)

    varr={}
    for tt in listt: 
      varr[tt]=filenc.variables[tt][:]
    return varr
    
    
def CalculateCoriolis(y_rho):
    """
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

def FindSimilar(num,arr):
    """ Finds most similiar value to number (num) in an array (arr)""" 
    arrtemp = np.absolute((arr-(num)))
    idd = np.where(arrtemp==min(arrtemp))
    return idd
