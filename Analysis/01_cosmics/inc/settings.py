#/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 18:48:06 2023

@author: Mattia Fanì (Los Alamos National Laboratory, US) - mattia.fani@cern.ch
Based on work of: 
    Francesco Pietropaolo (CERN)
    Serhan Tufanli (CERN)
    Chris Macias (University of Iowa, US)
    Furkan Dolek (Cukurova University, TR, and CERN)

"""

def settings():

    global N_EXPECTED_EVTS_PER_RAW_FILE
    global COLLECTION_BIAS_VOLTAGE
    global CATHODE_HV
    global chanPhy
    global IGNORED_FOLDER_PREFIX
    global N_EVTS_PER_CONV_FILE
    global N_TIME_TICKS
    global N_CHANNELS
    global output_align
    
    IGNORED_FOLDER_PREFIX = "."
        
    N_EXPECTED_EVTS_PER_RAW_FILE = 25
    
    COLLECTION_BIAS_VOLTAGE = 900 # Volts
    
    CATHODE_HV = 27200 # Volts
    
    N_EVTS_PER_CONV_FILE = 10 # Evt Nr for each .JSON file 
    
    N_TIME_TICKS = 645
    N_CHANNELS = 128
    
    output_align = '                   ' # only for cosmetics
    
    chanPhy = [24, 23,127, 22, 21, 49, 20, 19, 18, 17,
               50, 16, 15, 51, 14, 13, 12, 11, 52, 10,
                9, 53,  8,  7,  6,  5, 54,  4,  3, 55, 
                2,  1, 72, 73, 74, 75, 76, 77, 78, 79, 
               80, 81, 82, 83, 84, 85, 86, 87, 56, 57, 
               58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 
               68, 69, 70, 71, 36, 35,121, 34, 33,122, 
               32, 31, 30, 29,123, 28, 27,124, 26, 25, 
               48, 47,117, 46, 45,118, 44, 43, 42, 41, 
              119, 40, 39,120, 38, 37,125,126,128, 88, 
               89, 90, 91, 92, 93, 94, 95, 96, 97, 98,
               99,100,101,102,103,104,105,106,107,108,
              109,110,111,112,113,114,115,116]
    
    
    
    
    
    
    