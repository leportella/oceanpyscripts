# -*- coding: utf-8 -*-
"""
General tools to help build graphics

@author: leportella
"""
import sys

sys.path.insert(0, '/home/leportella/scripts/py/my/oceanpy/tools')

from generaltools import to_percent
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from windrose import WindroseAxes

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