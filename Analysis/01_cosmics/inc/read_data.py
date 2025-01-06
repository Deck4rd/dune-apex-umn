#/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 18:48:06 2023

@author: Mattia Fanì (Los Alamos National Laboratory, US) - mattia.fani@cern.ch

"""

import os
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
import json
import inc.settings
from inc.display_events import display_events

from inc.find_run_time import find_time_now
from os import makedirs
from inc.remove_coherent_noise import remove_coherent_noise

def read_data(pathToJsonFolder, fileName, dataType, plotDir, event_display, singleChannelDisplay):
    
    makedirs(plotDir, exist_ok = True)
    inc.settings.settings()
    print ('\n ['+find_time_now()+']'+' > Event display starts')
    
    # check folder, open all json files
    for (dirpath, dirnames, filenames) in os.walk(pathToJsonFolder):
        
        dirnames.sort()
        filenames.sort()

        for jsonFile in filenames:
            if jsonFile[-5:] == ".json":
                print(f'{inc.settings.output_align}> Reading file {jsonFile}')
                
                # Excluding hidden files
                if jsonFile.startswith(inc.settings.IGNORED_FOLDER_PREFIX):
                    continue
                with open(pathToJsonFolder+jsonFile) as f:
                    data = json.load(f)
                if len(data[dataType])==0:
                    continue
                    # print(f"{inc.settings.output_align}! ERROR: Input list is empty")
                    
                else:
                    evt_nr_mismatch = False
                    
                    # loop over events = lines of the json file
                    for i in range (0,len(data[dataType])):
                        
                        saveFileName=plotDir+"/"+jsonFile[:-5]+"_"+str(data[dataType][i]['convertedEventID'])+".pdf"
                        
                        evt_title = 'ID: ' +str(data[dataType][i]['eventId'])+\
                        ' ('+str(data[dataType][i]['binaryFileID'])+\
                        ', '+str(data[dataType][i]['binaryEventID'])+\
                        ') ('+str(data[dataType][i]['convertedFileID'])+\
                        ', '+str(data[dataType][i]['convertedEventID'])+\
                        ')'
                        
                        # Remove coherent noise 
                        data[dataType][i] = remove_coherent_noise(False, True, False, data[dataType][i],evt_title,saveFileName)
                        
                        # Event Display
                        if event_display: display_events(data[dataType][i],evt_title,saveFileName,evt_nr_mismatch,singleChannelDisplay)
                        
                        # Charge equalization on collection wires
                        
                        
