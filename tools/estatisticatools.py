# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 10:00:02 2016

@author: leportella
"""

import math
import numpy as np

def calcula_ema(medido, modelado):
    ''' Calcula o erro médio absoluto (Wilmott, 1982)
        ema = calcula_ema(nmedido,nmodelado)
        
        nmedido = vetor de dados medido
        nmodelaod = vetor de dados modelados
    '''

    if len(medido) != len(modelado):
        print('dados não tem mesmo tamanho!')
        return

    sum_errors=0
    medido = np.array(medido)
    modelado = np.array(modelado)
    
    for i in range(len(medido)):
        sum_errors += abs(modelado[i]-medido[i])
        
    ema = sum_errors/len(medido)
    
    return ema
    
def calcula_remq(medido, modelado):
    ''' Calcula a raiz do erro médio quadrático (Wilmott, 1982)
        remq = calcula_remq(nmedido,nmodelado)
        
        nmedido = vetor de dados medido
        nmodelaod = vetor de dados modelados
    '''

    if len(medido) != len(modelado):
        print('dados não tem mesmo tamanho!')
        return    

    medido = np.array(medido)
    modelado = np.array(modelado)
    
    sum_errors=0
    for i in range(len(medido)):
        sum_errors += ((modelado[i]-medido[i])**2)
    remq = math.sqrt(sum_errors/len(medido))
    
    return remq
    
def calcula_ia(medido, modelado):
    ''' Calcula a index of agreement (Wilmott, 1982)
        ia = calcula_ia(nmedido,nmodelado)
        
        nmedido = vetor de dados medido
        nmodelaod = vetor de dados modelados
    '''

    if len(medido) != len(modelado):
        print('dados não tem mesmo tamanho!')
        return    
    
    medido = np.array(medido)
    modelado = np.array(modelado)
    media_medidos = np.mean(medido) # O médio  na fórmula
    media_modelados = np.mean(modelado)       

    soma1=0
    soma2=0
    for i in range(len(medido)):
        soma1 = soma1 + (modelado[i]-medido[i])**2
        soma2 = soma2 + (abs(modelado[i]-media_modelados) + abs(medido[i]-media_medidos))**2
    
    ia = 1 - (soma1/soma2)
    
    return ia