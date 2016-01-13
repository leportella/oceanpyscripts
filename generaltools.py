# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:45:20 2015

Practical tools for day to day use

@author: leportella
"""

import numpy as np
import csv
from math import *

def FindSimilar(num,arr):
    """ Finds most similiar value to number (num) in an array (arr)
        
        out = FindSimilar(20,vector)
        
        out is the id where in vector there is a similar number
    """ 
    arrtemp = np.absolute((arr-(num)))
    idd = np.where(arrtemp==min(arrtemp))
    return idd,
    
def uv2veldir(u,v):
    """ 
    out = uv2veldir(u,v)

    Convert a u and v velocity to velocity and direction information.
    
    Based on this explanation:
    http://wx.gmu.edu/dev/clim301/lectures/wind/wind-uv.html
    
    Result:
    
    out['vel'] --> velocity
    out['dir'] --> direction
    """
    vel = []; direc=[]
    for i in range(0,len(u)):
        vel.append(sqrt((u[i]**2)+(v[i]**2)))
        direc.append(degrees(atan2(u[i],v[i])))
    att = {'vel':vel,'dir':direc}
    return att    
    
def csv2array(csv,csvdel=';',inline=0):
    """
        Read an csv to a numpy array with float numbers
        out = csv2array(csv,csvdel,inline)        
       
        where
        csv = 'csvfile.csv'
        csvdel is the csv delimiter, default is ';'
        inline is the initial line, default is 0    
        
    """
    out = np.array(list(csv.reader(open(csv,'rb'),delimiter=csvdel))[inline:],dtype=np.float64)
    return out

    
    