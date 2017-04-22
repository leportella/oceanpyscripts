#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: leportella

This is a script created for my master degree. This is an analysis of
current data from 3 Acoustic Doppler Current Profiler (ADCP), which is a
oceanographic equipment for measuring temperature, waterlevel and velocity
components of current (u and v).

This script focused on the formatting and graphic analysis of current
components.
"""

from datetime import datetime, timedelta
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from generaltools import uv2veldir, FindSimilar
from GraphicTools import plotaWindRose


WD = '/home/leportella/Documents/master/'
directory = '{}dados/utilizacao/'.format(WD)
outputDirectory = '{}dissertacao/Latex/dis_controlada/figuras/'.format(WD)

# ANALYSING DATA FROM 3 ADCPs EQUIPMENTS

# Read CSV files
csv01 = csv.reader(open(directory + 'ST001_Corrente.csv', 'r'), delimiter=',')
csv02 = csv.reader(open(directory + 'ST002_Corrente.csv', 'r'), delimiter=',')
csv03 = csv.reader(open(directory + 'ST003_Corrente.csv', 'r'), delimiter=',')

# Transform CSV to array
ST001 = np.array(list(csv01)[1:], dtype=np.float64)
ST002 = np.array(list(csv02)[1:], dtype=np.float64)
ST003 = np.array(list(csv03)[1:], dtype=np.float64)

# Create empty dictionary for data storage
STs = {1: ST001, 2: ST002, 3: ST003}
sts = {k: None for k in range(1, 4)}

# Formatting csv from data into dictionaries
for k in range(1, 4):
    time = []
    rep = STs[k]

    # transform date columns integers into datefield for time vector
    for i in range(0, len(rep)):
        time.append(
            datetime(
                int(rep[i, 2]), int(rep[i, 1]), int(rep[i, 0]),
                int(rep[i, 3]), int(rep[i, 4]), int(rep[i, 5])
            )
        )

    # ST003 is in UTC time, we should put it into local time
    if k == 3:
        localtime = np.subtract(time, timedelta(hours=3))
        localtime = pd.Series(localtime)
        sts[k] = {'tempo': localtime}
    else:
        time = pd.Series(time)
        sts[k] = {'tempo': time}

    # Each equipment has different layers of velocity to be studied
    # This defines the length of layers to consider
    lim = len(STs[k][0])
    numcels = (lim-6)/2
    c = 1

    # Read components u and v from current velocity considering
    # each layer of equipment
    for n in range(6, lim-1, 2):

        # get u and v from current layer
        u = pd.Series(rep[:, n])
        v = pd.Series(rep[:, n+1])

        # add unkown data as NaN
        u[u > 990] = np.nan
        v[v > 990] = np.nan

        # Interpolate data for continuous vector
        sts[k]['ucomp%s' % c] = u.interpolate()
        sts[k]['vcomp%s' % c] = v.interpolate()

        # Convert uv to velocity and direction
        out = uv2veldir(sts[k]['ucomp%s' % c], sts[k]['vcomp%s' % c])

        # Add data to dictionary
        sts[k]['vel%s' % c] = out['vel']
        sts[k]['dir%s' % c] = out['dir']

        # Plot current rose per layer
        plotaWindRose(out['dir'], out['vel']*100, maxYlabel=28, maxLeg=40,
                      stepLeg=5, language='en')
        name = '{}CurrentRose_ST00{}_Cel{}.png'.format(
            outputDirectory, str(k), str(c))
        plt.savefig(name, dpi=200)

        # get count
        c += 1

    # CALCULATING DEPTH AVERAGE CURRENT

    # Seggregate data
    series = pd.DataFrame(sts[k])
    us = [col for col in series if 'ucomp' in col]
    vs = [col for col in series if 'vcomp' in col]

    # Find depth average components u and v
    sts[k]['u_depthav'] = series[us][:].mean(axis=1)
    sts[k]['v_depthav'] = series[vs][:].mean(axis=1)

    # Calculate velocity and direction of depth avarage
    out2 = uv2veldir(sts[k]['u_depthav'], sts[k]['v_depthav'])

    # Add results in dictionary
    sts[k]['vel_depthav'] = out2['vel']
    sts[k]['dir_depthav'] = out2['dir']
    sts[k]['vel_depthav_cm'] = sts[k]['vel_depthav']*100

    # Create figure of depth average current acumulated histogram
    plt.figure()
    n, bins, patches = plt.hist(sts[k]['vel_depthav'], 100, normed=1,
                                histtype='step', cumulative=True, color='b')

    # find percentages values for adding percentage lines in the histogram
    n90 = FindSimilar(0.9, n)
    n50 = FindSimilar(0.5, n)
    n25 = FindSimilar(0.25, n)
    plt.plot([bins[n90[0][0]]]*2, [0, 0.9], 'k')
    plt.plot([0, bins[n90[0][0]]], [0.9, 0.9], 'k')

    plt.plot([bins[n50[0][0]]]*2, [0, 0.5], 'k')
    plt.plot([0, bins[n50[0][0]]], [0.5, 0.5], 'k')

    plt.plot([bins[n25[0][0]]]*2, [0, 0.25], 'k')
    plt.plot([0, bins[n25[0][0]]], [0.25, 0.25], 'k')
    plt.grid(True)
    plt.ylim(0, 1.05)
    plt.xlim(0, np.max(sts[k]['vel_depthav']))
    plt.xlabel('Velocity - m/s')
    plt.ylabel('Percentual')
    title = 'Acumulated  Histogram of Current Velocity - ST00{}'.format(k)
    plt.title(title)
    filename = '{}ST00{}_His_DepthAverageVel.png'.format(outputDirectory, k)
    plt.savefig(filename, dpi=200)

    # create depth average current quiver plots
    fig, (ax0, ax1) = plt.subplots(nrows=2,
                                   sharey=False,
                                   sharex=False,
                                   figsize=(11, 5))

    q = ax0.quiver(sts[k]['u_depthav'][::3],
                   sts[k]['v_depthav'][::3],
                   scale=4.5)
    p = plt.quiverkey(q, 1480, 0.04, 0.1, "0.1 m/s", coordinates='data',
                      color='k')
    ax0.axes.get_yaxis().set_visible(False)
    ax0.axes.get_xaxis().set_visible(False)
    ax0.set_ylim(-0.09, 0.09)
    ax0.set_xlim(0, len(sts[k]['u_depthav'][::3]))
    ax0.set_title('Current Vectors - ST00' + str(k))

    ax1.plot(sts[k]['tempo'], sts[k]['vel_depthav'])
    ax1.grid()
    ax1.set_ylim(0, 0.42)
    ax1.set_ylabel('Velocity (m/s)')
    ax1.set_xlabel('Time')
    ax1.set_title('Current Velocity - ST00' + str(k))
    fig_name = 'Corrente_Quiver_ST00' + str(k) + '3em3.png'
    plt.savefig(outputDirectory + fig_name, dpi=200)


# RESIDUAL CURRENT ANALYSIS EVERY 50 HOURS
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3,
                                    sharey=False,
                                    sharex=False,
                                    figsize=(11, 5))

q = ax0.quiver(sts[1]['uresidual_50h'],
               sts[1]['vresidual_50h'],
               scale=0.8,
               width=0.005)
p = plt.quiverkey(q, 29, 0.05, 0.05, "0.05 m/s", coordinates='data', color='k')
ax0.axes.get_yaxis().set_visible(False)
ax0.axes.get_xaxis().set_visible(False)
ax0.set_ylim(-0.02, 0.08)
ax0.set_xlim(0, len(sts[1]['uresidual_50h']))
ax0.set_title('Residual Current - 50h - ST001', fontsize=12)

q = ax1.quiver(sts[2]['uresidual_50h'],
               sts[2]['vresidual_50h'],
               scale=0.8,
               width=0.005)
p = plt.quiverkey(q, 29, 0.05, 0.05, "0.05 m/s", coordinates='data', color='k')
ax1.axes.get_yaxis().set_visible(False)
ax1.axes.get_xaxis().set_visible(False)
ax1.set_ylim(-0.02, 0.08)
ax1.set_xlim(0, len(sts[2]['uresidual_50h']))
ax1.set_title('Residual Current - 50h - ST002', fontsize=12)

q = ax2.quiver(sts[3]['uresidual_50h'],
               sts[3]['vresidual_50h'],
               scale=0.8,
               width=0.005)
p = plt.quiverkey(q, 29, 0.05, 0.05, "0.05 m/s", coordinates='data', color='k')
ax2.axes.get_yaxis().set_visible(False)
ax2.axes.get_xaxis().set_visible(True)
ax2.set_ylim(-0.02, 0.08)
ax2.set_xlim(0, len(sts[3]['uresidual_50h']))
ax2.set_title('Residual Current - 50h - ST003', fontsize=12)

labels = [item.get_text() for item in ax2.get_xticklabels()]
labels[0] = '0 h'
labels[1] = '250 h'
labels[2] = '500 h'
labels[3] = '750 h'
labels[4] = '1000 h'
labels[5] = '1250 h'
labels[6] = '1500 h'
ax2.set_xticklabels(labels)

filename = outputDirectory + 'Measured_Residual_Current_every_50h.png'
plt.savefig(filename, dpi=200)
