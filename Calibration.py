# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 19:16:05 2016

@author: leportella
"""
import sys

sys.path.insert(0,'/home/leportella/scripts/pyscripts/myscripts/open')

import netCDF4 as nc
import numpy as np
from generaltools import *
from ncwork import *
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pyproj import Proj

direct = '/home/leportella/Documents/master/dados/utilizacao/'
dirOut = '/home/leportella/Documents/master/dissertacao/Latex/dis_controlada/figuras/'


sts = {k: None for k in range(1, 4)}
loc = {k: None for k in range(1, 4)}
for k in range(1,4):
    sts[k] = pd.read_csv(direct+'DF_NivelTemp_' + str (k) + '.csv')

loc[1] = [26.7682, 48.6543]
loc[2] = [26.7643, 48.6617]
loc[3] = [26.7051, 48.6157]

r = nc.Dataset('/home/leportella/cluster/testes_iniciais/teste09/ocean_his_local.nc','r')
lonr = r.variables['lon_rho'][:]
latr = r.variables['lat_rho'][:]
zeta = r.variables['zeta'][:]



