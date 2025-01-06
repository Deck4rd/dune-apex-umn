#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 16:31:04 2023

@author: Mattia Fanì (Los Alamos National Laboratory, US) - mattia.fani@cern.ch

"""

for c_strip_index in range(9, 22):

    # if c_strip_index == 16:
    if c_strip_index == 15 or c_strip_index == 16:
        print(f"Condition == True: {c_strip_index}")
    elif 9 < c_strip_index < 22:
        print(c_strip_index)
