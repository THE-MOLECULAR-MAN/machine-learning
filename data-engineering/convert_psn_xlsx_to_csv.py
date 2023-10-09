#!/usr/local/bin/python3
# Tim H 2023

# python3 convert_psn_xlsx_to_csv.py -i '/Users/tim/tmp_datalake/entertainment-gaming-psn-2019-08-01_to_2023-09-14.xlsx'
# less '/Users/tim/tmp_datalake/entertainment-gaming-psn-2019-08-01_to_2023-09-14.csv'

"""Converts an Excel XLSX spreadsheet downloaded from Sony Playstation Network
into a usable CSV file for a data lake"""

import csv
import sys
import getopt
import pathlib
import warnings
import pandas as pd

from homelab_data_engineering import add_year_week_of_column


def main(argv):
    """main"""

    # disable warnings:
    # https://www.dataquest.io/blog/settingwithcopywarning/
    pd.set_option('mode.chained_assignment', None)
    # https://stackoverflow.com/questions/64420348/ignore-userwarning-from-openpyxl-using-pandas
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

    data_file = ''
    csv_filename = ''
    opts, args = getopt.getopt(argv, "hi:o:", ["xlsx_path="])
    for opt, arg in opts:
        if opt == '-h':
            print('convert_psn_xlsx_to_csv.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            # load the path to the Excel sheet as a command line argument
            data_file = arg
            csv_filename = pathlib.Path(data_file).with_suffix('.csv')

    # define the column names of the original xlsx file, in the order they
    # appear
    new_column_names = ['Game_Name', 'date',
                        'Entertainment_Gaming_PS5_PSN_Online_Activity_Seconds',
                        'Number_of_PSN_Online_Gaming_sessions']

    # read an excel file and convert
    handle = pd.read_excel(data_file, sheet_name=3, names=new_column_names)

    # convert into a dataframe object
    df_working = pd.DataFrame(handle)

    # delete the unused rows
    df_working = df_working.drop([0, 1, 2])

    # convert the columns to the proper data types
    df_working['date'] = pd.to_datetime(df_working['date'])
    df_working['Entertainment_Gaming_PS5_PSN_Online_Activity_Seconds'] = pd.to_numeric(
        df_working['Entertainment_Gaming_PS5_PSN_Online_Activity_Seconds'])

    # sort the dataframe by the date, ascending
    df_working = df_working.sort_values(by='date')
    df_working['Entertainment_Gaming_PS5_PSN_Online_Activity_Minutes'] = \
        df_working['Entertainment_Gaming_PS5_PSN_Online_Activity_Seconds'].div(
            60.0).round(2)

    df_working = df_working.drop(
        ['Entertainment_Gaming_PS5_PSN_Online_Activity_Seconds',
         'Game_Name', 'Number_of_PSN_Online_Gaming_sessions'], axis=1)

    # create the new column
    add_year_week_of_column(df_working)

    # change the order of the columns
    df_working = df_working[['date', 'year_week_number',
                             'Entertainment_Gaming_PS5_PSN_Online_Activity_Minutes']]

    # export to csv
    df_working.to_csv(csv_filename, header=True, index=False,
                      quoting=csv.QUOTE_NONNUMERIC)

    print(csv_filename)


if __name__ == "__main__":
    main(sys.argv[1:])
