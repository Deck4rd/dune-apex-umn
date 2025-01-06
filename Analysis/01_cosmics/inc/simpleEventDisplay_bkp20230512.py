#/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 18:48:06 2023

@author: Mattia Fanì (Los Alamos National Laboratory, US) - mattia.fani@cern.ch

"""

import os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
import json
import inc.settings

from inc.find_run_time import find_time_now
from os import makedirs
from inc.findPeaks import findPeaks
from inc.remove_coherent_noise import remove_coherent_noise
from inc.singleEvtDisplay import nicerSingleEvtDisplay

def most_frequent(List): 
    return max(set(List), key = List.count) 

def displayEvents(pathToJsonFolder, fileName, dataType, plotDir, singleChannelDisplay):
    
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
                        mostFreqADC = 0
                        adc=np.empty((inc.settings.N_TIME_TICKS,inc.settings.N_CHANNELS)) 
                        
                        evt_title = 'ID: ' +str(data[dataType][i]['eventId'])+\
                        ' ('+str(data[dataType][i]['binaryFileID'])+\
                        ', '+str(data[dataType][i]['binaryEventID'])+\
                        ') ('+str(data[dataType][i]['convertedFileID'])+\
                        ', '+str(data[dataType][i]['convertedEventID'])+\
                        ')'
                        
                        #######################################################
                        # Remove coherent noise 
                        #######################################################
                        
                        data[dataType][i] = remove_coherent_noise(False, True, False, data[dataType][i],evt_title,saveFileName)
                        
                        #######################################################
                        # Event Display
                        #######################################################
                        
                        for ichn in range(128): 
                            channel = 'chn'+str(ichn)
                            
                            mostFreqADC = most_frequent(data[dataType][i][channel])
                            
                            if len(np.array(data[dataType][i][channel])) != 645:
                                print(f'{inc.settings.output_align}! len(data[{dataType}][{i}][{channel}]) = '
                                      f'{len(np.array(data[dataType][i][channel]))} instead of '
                                      f'{inc.settings.N_TIME_TICKS}. Channel skipped')
                                evt_nr_mismatch == True
                                continue
                            else:
                                adc[:,ichn] = np.array(data[dataType][i][channel])-mostFreqADC

                                peaks, properties = findPeaks(adc[:,ichn], ichn)  
                                if singleChannelDisplay and ichn < 128:
                                    nicerSingleEvtDisplay(ichn, adc[:,ichn], peaks, saveFileName[:-4], evt_title, True)
                        
                        # Setting image quality 
                        # Disegard IDEs' unused local variable warning
                        fig = plt.figure(figsize=(16,8),dpi=100) 
                        plt.pcolor(adc, vmin=-100, vmax=100)             
                        plt.colorbar()
                        plt.xlabel('Channels'),plt.ylabel('Time ticks [0.5us/tick]')
                        plt.title(data[dataType][i]['runTime']+ ' - ' + evt_title)
                        plt.xticks(np.arange(0, 129, 10))                              
                        
                        if os.path.isfile(saveFileName) == False:
                        
                            plt.savefig(saveFileName)
                            plt.show()  #!!! Need to adapt this line to lxplus

                        print (f' [{find_time_now()}] : {saveFileName} file created')
                        
                        plt.clf()
                        plt.close()
        
    print ( ' ['+find_time_now()+']'+" > Event display completed")
