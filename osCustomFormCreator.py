#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 07:03:29 2023

@author: krishagni
"""

import configparser, pandas as pd

#### Call config object #########
config_obj = configparser.ConfigParser()

#### Read Config file ###########
config_obj.read("configfile.ini")

#### Read path from input file from Config file ##############
path_of_input_file = config_obj["input_file_path"]["path_of_input_file"]
path_of_output_folder = config_obj["output_folder"]["path_of_output_folder"]
module = config_obj["module"]["module_type"]

#### Read input file using pandas module ################
rawData = pd.read_csv(path_of_input_file, sep = ',' , low_memory = False)
rawData['Field_Name'] = rawData['Form_Name'] + '#' + rawData['Field_Name']

#### Group the data by Form_Name #######
groups = rawData.groupby('Form_Name')

for formName, group in groups:    
    #### Pivot the DataFrame to reshape #######
    df_pivot = group.pivot_table(index=['CP_Title', module], columns='Field_Name', values='Field_Value', aggfunc='first')  
    #### Takes the first value if there are multiple values for a given combination of index and column.
    
    #### Reset the index to turn the MultiIndex into columns ####
    df_pivot = df_pivot.reset_index()
    
    #### Output csv files ######
    df_pivot.to_csv(f'{path_of_output_folder}/{formName}.csv')
