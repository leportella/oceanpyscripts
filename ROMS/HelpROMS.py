# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 19:36:19 2016

@author: leportella
"""

def FindTS(dt,dias):
    """
    FindTS(dt,dias)
    
    dt = delta t do modelo em segundos
    dias = numero de dias que o modelo vai rodar
    """
    totalsegundos = dias * 24 * 60 * 60
    numts = totalsegundos/float(dt)
    print 'Numero de ts: ' + str(numts)

def FindNHIS(dt,hora=1):
    """
    """
    nhis = (hora*60*60.)/(float(dt))
    print 'Numero para NHIS: ' + str(nhis)
    
   
dt=30
FindTS(dt,40)   
FindNHIS(dt,1)