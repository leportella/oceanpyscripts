# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 10:00:02 2016

@author: leportella
"""

import math
import numpy as np

def calcula_ema(nmedido,nmodelado):
    ''' Calcula o erro médio absoluto (Wilmott, 1982)
        ema = calcula_ema(nmedido,nmodelado)
        
        nmedido = vetor de dados medido
        nmodelaod = vetor de dados modelados
    '''
    
    ema=0
    for i in range(len(nmedido)):
        ema = ema + abs(nmodelado[i]-nmedido[i])
        
    ema = ema/len(nmedido)
    
    return ema
    
def calcula_remq(nmedido,nmodelado):
    ''' Calcula a raiz do erro médio quadrático (Wilmott, 1982)
        remq = calcula_remq(nmedido,nmodelado)
        
        nmedido = vetor de dados medido
        nmodelaod = vetor de dados modelados
    '''
    
    remq=0
    for i in range(len(nmedido)):
        remq = remq + ((nmodelado[i]-nmedido[i])**2)
    remq = math.sqrt(remq/len(nmedido))
    
    return remq
    
def calcula_ia(nmedido,nmodelado):
    ''' Calcula a index of agreement (Wilmott, 1982)
        ia = calcula_ia(nmedido,nmodelado)
        
        nmedido = vetor de dados medido
        nmodelaod = vetor de dados modelados
    '''
    
    media_medidos = np.mean(nmedido) # O médio  na fórmula
    media_modelados = np.mean(nmodelado)       

    soma1=0
    soma2=0
    for i in range(len(nmedido)):
        soma1 = soma1 + (nmodelado[i]-nmedido[i])**2
        soma2 = soma2 + (abs(nmodelado[i]-media_modelados) + abs(nmedido[i]-media_medidos))**2
    
    ia = 1 - (soma1/soma2)
    
    return ia