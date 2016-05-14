#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 16:34:06 2015

@author: leportella

out = uv2veldir(u,v)

Convert a u and v velocity to velocity and direction information.

Based on this explanation:
http://wx.gmu.edu/dev/clim301/lectures/wind/wind-uv.html

Result:

out['vel'] --> velocity
out['dir'] --> direction

"""

def uv2veldir(u,v):
    vel = []; direc=[]
    for i in range(0,len(u)):
        vel.append(sqrt((u[i]**2)+(v[i]**2)))
        direc.append(degrees(atan2(u[i],v[i])))
    att = {'vel':vel,'dir':direc}
    return att