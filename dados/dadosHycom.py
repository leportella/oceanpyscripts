# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 11:10:09 2015

@author: leportella
"""


import netCDF4 as nc
import numpy as np
from ncwork import *

arq = nc.Dataset('http://tds.hycom.org/thredds/dodsC/GLBu0.08/expt_19.1/2012/3hrly','r')

lon = arq.variables['lon'][:]
lat = arq.variables['lat'][:]

ilat, = FindSimilar(-20,lat)
flat, = FindSimilar(-40,lat)
ilon, = FindSimilar(-38,lon)
flon, = FindSimilar(-56,lon)



sal = arq.variables['salinity'][1,:,int(flat):int(ilat),int(flon):int(ilon)]