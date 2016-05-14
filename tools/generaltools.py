# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:45:20 2015

Practical tools for day to day use

@author: leportella
"""

import numpy as np
import csv
from math import *
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FuncFormatter
import pandas as pd
from windrose import WindroseAxes

   

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

def to_percent(y, position):
# Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] is True:
        return s + r'$\%$'
    else:
        return s + '%'


class PercentHistogram(object):
        
    def __init__(self,inputdata,binss=10,size=(15,5)):
        plt.figure(figsize=size)
        plt.hist(inputdata[~np.isnan(inputdata)],bins=binss, normed=True)
        formatter = FuncFormatter(to_percent)
        plt.show()
    

def new_axes():
   fig = plt.figure(figsize=(15, 10), dpi=100, facecolor='w', edgecolor='w')
   rect = [0.1, 0.1, 0.8, 0.8]
   ax = WindroseAxes(fig, rect, axisbg='w')
   fig.add_axes(ax)
   return ax

def plotaWindRose(direc, vel, maxYlabel, maxLeg, stepLeg=1, stepYlabel=5, fonte=18, language='pt'):
    """
    Plots a well ajusted WindRose 
    
    plotaWindRose(direction, velocity, maxYabel=20, maxLeg=0.5, stepLeg=1, stepYlabel=5, fonte=18, language='pt')  

    direction = time series of direction
    velocity = time series of velcities
    maxYlabel = maximum value of percentage to be shown in the y axis
    maxLeg = maximum value of the time series to be represented on the legend
    stepLeg = interval which the legend should be made
    stepYlavel = interval which the legend shold be made
    fonte = fontsize of the labels  
    language = which language should be made ('pt' for portuguese, 'en', for english)
    
    """    
    
    ax = new_axes()
    ax.bar(direc,vel,
           normed=True, 
           opening=0.8, 
           edgecolor='white',
           bins = np.arange(0.00,maxLeg,stepLeg))
    l = ax.legend(bbox_to_anchor=(1.05, 0.6))
    plt.setp(l.get_texts(), fontsize=fonte)
    ax.set_rlabel_position(130)
    ax.set_yticks(range(0, maxYlabel, stepYlabel))  
    ax.set_yticklabels(map(str, range(0, maxYlabel, stepYlabel)),fontsize=fonte)

    if language=='pt':
        ax.set_xticklabels(['L', 'NE', 'N', 'NO', 'O', 'SO', 'S', 'SE'],fontsize=fonte)
    else:
        ax.set_xticklabels(['L', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE'],fontsize=fonte)