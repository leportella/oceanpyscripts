# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 23:49:31 2016

@author: leportella
"""


import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

m = Basemap(projection='cyl', resolution='f', llcrnrlon= -48.7, llcrnrlat= -26.8, urcrnrlon= -48.55, urcrnrlat= -26.65)

loc = {k: None for k in range(1, 4)}

loc[1] = {'lat': -26.7682, 'lon': -48.6543}
loc[2] = {'lat': -26.7643, 'lon': -48.6617}
loc[3] = {'lat': -26.7051, 'lon': -48.6157}

fig = plt.figure()
m.drawcoastlines(linewidth=0.25,color = 'k')
m.fillcontinents(color='0.8',lake_color='aqua')
m.plot(loc[1]['lon'],loc[1]['lat'], 'bo', markersize=10,label='ST001')
m.plot(loc[2]['lon'],loc[2]['lat'], 'b^', markersize=10,label='ST002')
m.plot(loc[3]['lon'],loc[3]['lat'], 'bs', markersize=10,label='ST003')

m.plot(-48.6048, -26.7862,'r*', markersize=10, label='Penha tide gauge')
leg = plt.legend(['ST001','ST002','ST003','Penha Tide Gauge'],numpoints=1)
#m.legend()
