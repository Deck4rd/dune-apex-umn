#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 17:32:38 2023

@author: Mattia Fanì (Los Alamos National Laboratory, USA) - mattia.fani@cern.ch

"""
import numpy as np
import json
import matplotlib.pyplot as plt

dataType="signalData"
folderName="20220502_test"

dirInputFile = "../DATA/"+folderName+"/jsonDATA/"
inFileName = "run01tri.json"

f = open(dirInputFile+inFileName)
data = json.load(f)

# for i in range (0,len(data[dataType])): # events
# # for i in range (6,7): # events
#     for x in range(24,25): # channels: 0-127
#         channel = 'chn'+str(x)
#         myArray = np.array(data[dataType][i][channel])
        
#         print("Evt",i,channel, myArray[:5],"...", myArray[-5:])
        
#         f.close
        

Np = 645 # points
iEvt = 31
iChn = 48

channel = 'chn'+str(iChn)

y = np.array(data[dataType][iEvt][channel])
print("Evt",iEvt,channel, y[:5],"...", y[-5:])

t = np.array(data[dataType][iEvt][channel])
dt=1/2 # us
Dt=Np*dt


dirOut = "./Plots/"+folderName

from pathlib import Path
Path(dirOut).mkdir(parents=True, exist_ok=True)

plotTitle = "Evt"+str(iEvt)+"Chn"+str(iChn)
outFileName = plotTitle+".pdf"

# Create the scatter plot

fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
ax.plot(np.arange(0,Dt,dt), t,label='line label', color='blue',\
        linewidth=2, linestyle='-', marker='o', markersize=2)

# Add labels and title
ax.set_xlabel('t [us]', fontsize=18)
ax.set_ylabel('ADC', fontsize=18)
ax.set_title(plotTitle, fontsize=20)

# Add a grid to the plot
ax.grid(True, linewidth=0.5, color='gray', linestyle='--')

# Save the plot to a file
fig.savefig(dirOut+"/"+outFileName)

# Display the plot
plt.show()


