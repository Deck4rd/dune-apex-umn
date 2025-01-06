#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 18:48:06 2023

@author: Mattia Fanì (Los Alamos National Laboratory, US) - mattia.fani@cern.ch

"""

# import os
# import json
import sys
import inc.settings
from pathlib import Path
from inc.read_data import read_data

DEFAULTS = {
    'input_conversion_bool': False,
    'input_evtdisplay_bool': True,
    'input_chndisplay_bool': True,
    'raw_data_folder_name': '20220511_dev01',
    # 'raw_data_folder_name': '20220511_all',
    'data_type': 'selectedEvents'
}

def main(raw_data_folder_name, input_data_type_int, input_conversion_bool,\
         input_evtdisplay_bool, input_chndisplay_bool):
    
    # LOADING TPC PARAMETERS
    inc.settings.settings()
    
    # SHOWING DATA TYPE MAP
    data_type_map = {
    0: 'displayAll',
    1: 'noiseData',
    2: 'signalData',
    3: 'selectedEvents'
    }
    
    data_type = data_type_map.get(input_data_type_int, DEFAULTS['data_type'])
    path_to_folder_converted_files = f"../../DATA/{raw_data_folder_name}/jsonData/"
    
    Path(path_to_folder_converted_files).mkdir(parents=True, exist_ok=True)
    
    # EVENT DISPLAY
    if input_evtdisplay_bool:
        path_to_folder_plots = f"./Plots/{raw_data_folder_name}"
        read_data(path_to_folder_converted_files, raw_data_folder_name,\
                      data_type, path_to_folder_plots, input_chndisplay_bool)

# ENABLING INPUT FROM TERMINAL
if __name__ == "__main__":
    inc.settings.settings()
    if len(sys.argv) == 6: 
        raw_data_folder_name  = sys.argv[1]
        input_data_type_int   = int(sys.argv[2])
        input_conversion_bool = bool(int(sys.argv[3]))
        input_evtdisplay_bool = bool(int(sys.argv[4]))
        input_chndisplay_bool = bool(int(sys.argv[5]))
    else:
        print(f'{inc.settings.output_align}! Arguments not found. Running with DEFAULT parameters')
        raw_data_folder_name  = DEFAULTS['raw_data_folder_name']
        input_data_type_int   = DEFAULTS['data_type']
        input_conversion_bool = DEFAULTS['input_conversion_bool']
        input_evtdisplay_bool = DEFAULTS['input_evtdisplay_bool']
        input_chndisplay_bool = DEFAULTS['input_chndisplay_bool']
        
    main(raw_data_folder_name, input_data_type_int, input_conversion_bool, input_evtdisplay_bool, input_chndisplay_bool)
