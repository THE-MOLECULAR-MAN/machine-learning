#!/usr/local/bin/python3
# Tim H 2023
"""This is a library of reused functions for my data engineering."""
# This script is not directly executable.
#
# import csv
# import sys
# import getopt
# import pandas as pd


import sys
import csv
import getopt
import pathlib

import pandas as pd



# __name__ = 'homelab_data_engineering'
# year_week_concatenator = '_wk_'
YEAR_WEEK_CONCATENATOR = '_wk_'


def add_year_week_of_column(dfx):
    """adds a new column to an existing Pandas dataframe that includes the
    year and week number. Used for easily doing group-by statements in 
    reporting"""
    # variables in Python are passed by reference, not value
    # Gotcha: dfx must have a column named 'date' that is of data type timestamp
    # define a constant that will join the year and week number

    # create the new column first,
    # initialize it to Not A Number as a string/object
    dfx['year_week_number'] = 'NAN'

    # iterate through each row
    for ind in dfx.index:
        # extract the year
        iter_year = dfx['date'][ind].year
        # determine the week number of that specific date
        iter_week_num = str(dfx['date'][ind].weekofyear).zfill(2)

        # create a new string that will hold the value:
        new_column_value = str(iter_year) + \
            YEAR_WEEK_CONCATENATOR + iter_week_num

        # assign it in-place:
        dfx['year_week_number'][ind] = new_column_value

def get_input_output_files(argv_param, new_suffix):
    """x"""
    # new_suffix must include the leading period: ex: .csv
    opts, args = getopt.getopt(argv_param, "hi:o:", ["i="])
    for opt, arg in opts:
        if opt == '-h':
            print('xxx.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input_filename = arg
            output_filename = pathlib.Path(input_filename).with_suffix(new_suffix)
            return input_filename, output_filename

def load_json_file_into_pandas_dataframe(input_filename):
    """x"""
    return pd.read_json(input_filename)

def output_dataframe_to_csv(df_working, output_filename):
    """x"""
    df_working.to_csv(output_filename, header=True, index=False,
              quoting=csv.QUOTE_NONNUMERIC)