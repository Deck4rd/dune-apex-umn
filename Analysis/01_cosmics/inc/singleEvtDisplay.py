#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:01:46 2023

@author: Mattia Fanì (Los Alamos National Laboratory, US) - mattia.fani@cern.ch
"""

import matplotlib.pyplot as plt
import inc.settings
import numpy as np

def singleEvtDisplay(chn,y,peaks):
    
    plt.plot(y, \
             label='FEMB_'+str(chn)+', chn_'+str(inc.settings.chanPhy[chn]))
    plt.plot(peaks, y[peaks], "x")
    plt.ylabel('ADC (baseline subtracted)')
    plt.xlabel('time ticks')
    plt.legend()
    plt.grid()
    plt.show()
    
def nicerSingleEvtDisplay(chn,y,peaks,saveFileName,evt_title,yrange):

    fig, ax = plt.subplots(figsize=(32, 9))

    ax.plot(y, label='FEMB_' + str(chn) + ', chn_' + str(inc.settings.chanPhy[chn]))
    ax.plot(peaks, y[peaks], "x")
    
    ax.set_ylabel('ADC (baseline subtracted)', labelpad=10, fontsize=24)  
    ax.set_xlabel('time ticks [0.5 µs/tick]', fontsize=24)
    ax.legend(fontsize=24)  

    # Primary grid on both x and y axes
    ax.grid(True, which='major', axis='both', linewidth=1, color='gray')

    # Secondary grid on x-axis
    ax.grid(True, which='minor', axis='x', linewidth=0.5, linestyle='dashed', color='gray')

    # Set x-axis ticks and minor ticks
    ax.set_xticks(np.arange(0, 645+1, 50))
    ax.set_xticks(np.arange(0, 645+1, 10), minor=True)

    # Set y-axis range and position
    if yrange == True:
        if chn < 48: ax.set_ylim(-20, 300)
        else: ax.set_ylim(-250, 250)
    
    ax.set_xlim(0, len(y))
    ax.yaxis.set_label_coords(-.04, 0.5)
    ax.spines['right'].set_visible(False)  

    plt.title(f"Chn_{chn} - {evt_title}", fontsize=30)

    # plt.subplots_adjust(left=0.06, right=0.94, top=0.96, bottom=0.08) 
    
    # plt.tight_layout()
    
    plt.savefig(f"{saveFileName} - Chn_{chn}"+'.pdf', dpi=100)

    plt.show()






