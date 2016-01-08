# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:45:20 2015

Practical tools for day to day use

@author: leportella
"""

import numpy as np
import csv


def FindSimilar(num,arr):
    """ Finds most similiar value to number (num) in an array (arr)
        
        out = FindSimilar(20,vector)
        
        out is the id where in vector there is a similar number
    """ 
    arrtemp = np.absolute((arr-(num)))
    idd = np.where(arrtemp==min(arrtemp))
    return idd,
    
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

    
    