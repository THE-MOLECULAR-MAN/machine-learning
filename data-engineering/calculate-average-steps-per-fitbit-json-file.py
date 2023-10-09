#!/usr/local/bin/python3
# Tim H 2023
"""x"""

import pprint
import glob
import os
import json


def load_json_file(filename):
    # print("load_json_file - will open file: " + filename)
    with open(filename, mode='r') as currentFile:
        # json.load is for files, json.loads is for strings
        return json.load(currentFile)


def sum_single_json_file(filename):
    sum_of_values = 0
    count_of_top_level_keys = 0
    
    json_data_as_list = load_json_file(filename)
    myinfo = json_data_as_list

    for item in myinfo:
        # TODO: check if the key exists before accessing it:
        if 'value' in item.keys() and str(item['value']).isnumeric():
            mycnt = int(item['value'])
            sum_of_values += mycnt
        count_of_top_level_keys += 1
        
    print(filename + " sum:" + str(sum_of_values) + " count: " + str(count_of_top_level_keys))


FITBIT_EXPORT_PATH = '/Users/tim/tmp_datalake/Exercise_Records/Tim-FitBit-export-2023-09-12/TimH/Physical Activity'
# jq '.[] | .value | tonumber' 'very_active_minutes-2023-02-28.json' | awk '{sum+=$0} END{print sum}'

for iter_filename in glob.glob(os.path.join(FITBIT_EXPORT_PATH, '*.json')):
    sum_single_json_file(iter_filename)

print("calculate-average-steps-per-fitbit-json-file.py finished successfully")
