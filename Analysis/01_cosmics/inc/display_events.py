#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 15:47:32 2023

@author: Mattia Fanì (Los Alamos National Laboratory, US) - mattia.fani@cern.ch

"""

import os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
import inc.settings

from inc.find_run_time import find_time_now
from inc.findPeaks import findPeaks
from inc.singleEvtDisplay import nicerSingleEvtDisplay

def most_frequent(List): 
    return max(set(List), key = List.count) 
    
def display_events(data,evt_title,saveFileName,evt_nr_mismatch,singleChannelDisplay):
    
    adc=np.empty((inc.settings.N_TIME_TICKS,inc.settings.N_CHANNELS)) 
    mostFreqADC = 0
    
    for ichn in range(128): 
        channel = 'chn'+str(ichn)
        
        mostFreqADC = most_frequent(data[channel])
        
        if len(np.array(data[channel])) != 645:
            print(f'{inc.settings.output_align}! len(data[{channel}]) = '
                  f'{len(np.array(data[channel]))} instead of '
                  f'{inc.settings.N_TIME_TICKS}. Channel skipped')
            evt_nr_mismatch == True
            continue
        else:
            adc[:,ichn] = np.array(data[channel])-mostFreqADC

            peaks, properties = findPeaks(adc[:,ichn], ichn)  
            if singleChannelDisplay and ichn < 128:
                nicerSingleEvtDisplay(ichn, adc[:,ichn], peaks, saveFileName[:-4], evt_title, True)
    
    # Setting image quality 
    # Disegard IDEs' unused local variable warning
    fig = plt.figure(figsize=(16,8),dpi=100) 
    plt.pcolor(adc, vmin=-100, vmax=100)             
    plt.colorbar()
    plt.xlabel('Channels'),plt.ylabel('Time ticks [0.5us/tick]')
    plt.title(data['runTime']+ ' - ' + evt_title)
    plt.xticks(np.arange(0, 129, 10))                              
    
    if os.path.isfile(saveFileName) == False:
    
        plt.savefig(saveFileName)
        plt.show()  #!!! Need to adapt this line to lxplus

    print (f' [{find_time_now()}] : {saveFileName} file created')
    
    plt.clf()
    plt.close()
    

