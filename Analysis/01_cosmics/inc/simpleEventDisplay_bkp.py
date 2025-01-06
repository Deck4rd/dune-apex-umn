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
from inc.singleEvtDisplay import singleEvtDisplay
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
                        # BLS
                        #######################################################
                        
                        common_baseline_C  = np.zeros(645)
                        common_baseline_i1 = np.zeros(645)
                        common_baseline_i2 = np.zeros(645)
                       
                        #determining the common baseline (only for cosmic data)
                        for t in range(645): 
                            ichn_count_C = 0
                            ichn_count_i1 = 0
                            ichn_count_i2 = 0
                            for ichn in range(128): 
                                channel = 'chn'+str(ichn)
                                if ichn < 48:
                                    if len(np.array(data[dataType][i][channel])) == 645:
                                        common_baseline_C[t] += data[dataType][i][channel][t]
                                        ichn_count_C += 1
                                elif ichn >= 48 and ichn < 88:
                                    if len(np.array(data[dataType][i][channel])) == 645:
                                        common_baseline_i1[t] += data[dataType][i][channel][t]
                                        ichn_count_i1 += 1
                                elif ichn >= 88:
                                    if len(np.array(data[dataType][i][channel])) == 645:
                                        common_baseline_i2[t] += data[dataType][i][channel][t]
                                        ichn_count_i2 += 1
                                        
                            common_baseline_C[t] = common_baseline_C[t]/ichn_count_C
                            common_baseline_i1[t] = common_baseline_i1[t]/ichn_count_i1
                            common_baseline_i2[t] = common_baseline_i2[t]/ichn_count_i2
                            
                        #subtracting the common baseline
                        for ichn in range(128): 
                            for t in range(645): 
                                channel = 'chn'+str(ichn)
                                if ichn < 48:
                                    data[dataType][i][channel][t] = data[dataType][i][channel][t]-common_baseline_C[t] 
                                    
                                elif ichn >= 48 and ichn < 88:
                                    data[dataType][i][channel][t] = data[dataType][i][channel][t]-common_baseline_i1[t]
                                    
                                elif ichn >= 88:
                                    data[dataType][i][channel][t] = data[dataType][i][channel][t]-common_baseline_i2[t]
                                           
                        nicerSingleEvtDisplay(0, common_baseline_C, [], saveFileName[:-4]+'BLc', 'BLc '+evt_title, False)
                        nicerSingleEvtDisplay(0, common_baseline_i1, [], saveFileName[:-4]+'BLi1', 'BLi1 '+evt_title, False)
                        nicerSingleEvtDisplay(0, common_baseline_i2, [], saveFileName[:-4]+'BLi2', 'BLi2 ' +evt_title, False)
               
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
                                    # singleEvtDisplay(ichn, adc[:,ichn], peaks)
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
