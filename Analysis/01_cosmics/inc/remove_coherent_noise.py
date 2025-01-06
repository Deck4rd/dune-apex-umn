#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 15:34:22 2023

@author: Mattia Fanì (Los Alamos National Laboratory, US) - mattia.fani@cern.ch

"""

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})

from inc.singleEvtDisplay import nicerSingleEvtDisplay

def remove_coherent_noise(b0,b1,b2,data,evt_title,saveFileName):
    
    common_baseline_C  = np.zeros(645)
    common_baseline_i1 = np.zeros(645)
    common_baseline_i2 = np.zeros(645)
   
    #determining the common baseline 
    for t in range(645): 
        ichn_count_C = -1
        ichn_count_i1 = -1
        ichn_count_i2 = -1
        for ichn in range(128): 
            channel = 'chn'+str(ichn)
            if ichn < 48 and b0 == True:
                if len(np.array(data[channel])) == 645:
                    common_baseline_C[t] += data[channel][t]
                    ichn_count_C += 1
            elif ichn >= 48 and ichn < 88 and b1 == True:
                if len(np.array(data[channel])) == 645:
                    common_baseline_i1[t] += data[channel][t]
                    ichn_count_i1 += 1
            elif ichn >= 88 and b2 == True:
                if len(np.array(data[channel])) == 645:
                    common_baseline_i2[t] += data[channel][t]
                    ichn_count_i2 += 1
                    
        if b0: common_baseline_C[t] = common_baseline_C[t]/ichn_count_C
        if b1: common_baseline_i1[t] = common_baseline_i1[t]/ichn_count_i1
        if b2: common_baseline_i2[t] = common_baseline_i2[t]/ichn_count_i2
        
    #subtracting the common baseline
    for ichn in range(128): 
        channel = 'chn'+str(ichn)
        for t in range(645): 
            if ichn < 48 and b0 == True:
                data[channel][t] = data[channel][t]-common_baseline_C[t] 
                
            elif ichn >= 48 and ichn < 88 and b1 == True:
                data[channel][t] = data[channel][t]-common_baseline_i1[t]
                
            elif ichn >= 88 and b2 == True:
                data[channel][t] = data[channel][t]-common_baseline_i2[t]
                       
    nicerSingleEvtDisplay(0, common_baseline_C, [], saveFileName[:-4]+'BLc', 'BLc '+evt_title, False)
    nicerSingleEvtDisplay(0, common_baseline_i1, [], saveFileName[:-4]+'BLi1', 'BLi1 '+evt_title, False)
    nicerSingleEvtDisplay(0, common_baseline_i2, [], saveFileName[:-4]+'BLi2', 'BLi2 ' +evt_title, False)

    
    return data
    