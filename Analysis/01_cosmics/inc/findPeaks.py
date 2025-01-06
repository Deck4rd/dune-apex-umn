#/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 09 18:48:06 2023

@author: Mattia Fanì (Los Alamos National Laboratory, US) - mattia.fani@cern.ch
Based on work of: 
    Francesco Pietropaolo (CERN)
    Serhan Tufanli (CERN)
    Chris Macias (University of Iowa, US)
    Furkan Dolek (Cukurova University, TR, and CERN)

"""

#import matplotlib.pyplot as plt

from scipy.signal import find_peaks

def findPeaks(data, chn):
    baselineValues = data.mean()
    withOutBaseline = data-baselineValues
    # pe,prop = find_peaks(withOutBaseline, height=18,width=5)
    pe,prop = find_peaks(withOutBaseline, height=18,width=5)
    
    #if len(pe)>0:
        # plot and check peaks visually
        # plt.plot(withOutBaseline, label='channel-'+str(chn))
        # plt.plot(pe, withOutBaseline[pe], "x")
        # plt.ylabel('ADC (baseline subtracted)')
        # plt.xlabel('time ticks')
        # plt.legend()
        # plt.grid()
        # plt.show()
    return pe,prop