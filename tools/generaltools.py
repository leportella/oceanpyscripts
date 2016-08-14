# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:45:20 2015

Practical tools for day to day use

@author: leportella
"""

import csv
from math import atan2, degrees, sqrt
import matplotlib
import numpy as np
import pandas as pd

def FindSimilar(num,arr):
    """ Finds most similiar value to number (num) in an array (arr)
        
        out = FindSimilar(20,vector)
        
        out is the id where in vector there is a similar number
    """ 
    arrtemp = np.absolute((arr-(num)))
    
    row,col = np.where(arrtemp==np.min(arrtemp))
    return row,col

def find_index_of_nearest_xy(y_array, x_array, y_point, x_point):
    distance = (y_array-y_point)**2 + (x_array-x_point)**2
    idy,idx = np.where(distance==distance.min())
    return idy[0],idx[0]

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
        direcao = degrees(atan2(u[i],v[i]))
        if direcao<0:
            direcao = direcao+360
        direc.append(direcao)
            
        
        att = {'vel':pd.Series(vel),'dir':pd.Series(direc)}
    return att    

def uv2veldir_wind(u,v):
    """ 
    out = uv2veldir_wind(u,v)

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
        direcao = degrees(atan2(u[i],v[i]))
        direcao-=180
        if direcao<0:
            direcao = direcao+360
        
        direc.append(direcao)
        att = {'vel':pd.Series(vel),'dir':pd.Series(direc)}
    return att    

def csv2array(csvfile, csvdel=';',inline=0):
    """
        Read an csv to a numpy array with float numbers
        out = csv2array(csv,csvdel,inline)        
       
        where
        csv = 'csvfile.csv'
        csvdel is the csv delimiter, default is ';'
        inline is the initial line, default is 0    
        
    """
    csvfile_reader = csv.reader(open(csvfile,'rb'),delimiter=csvdel)
    out = np.array(list(csvfile_reader)[inline:],dtype=np.float64)
    return out

def to_percent(y, position):
# Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] is True:
        return s + r'$\%$'
    else:
        return s + '%'


