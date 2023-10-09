#!/usr/local/bin/python3
# Tim H 2023
"""converts a list of date ranges in CSV format to a list of individual dates
and marks them as travel/vacation days"""

# python3 convert_date_ranges_to_date_list.py -i '/Users/tim/tmp_datalake/travel_date_ranges.csv'
# less '/Users/tim/tmp_datalake/travel_date_ranges.csv-list.csv'

import csv
import sys
import getopt
from datetime import timedelta
import pandas as pd

from homelab_data_engineering import YEAR_WEEK_CONCATENATOR


def main(argv):
    """main"""
    # load arguments from command line
    input_filename = ''
    output_filename = ''
    opts, args = getopt.getopt(argv, "hi:o:", ["i="])
    for opt, arg in opts:
        if opt == '-h':
            print('convert_date_ranges_to_date_list.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input_filename = arg
            output_filename = input_filename + "-list.csv"

    # load the CSV into a pandas dataframe
    df_ranges = pd.read_csv(input_filename, header=0)

    # convert the datatypes for the date columns to timestamps
    df_ranges['Travel_Start_Date'] = pd.to_datetime(
        df_ranges['Travel_Start_Date'])
    df_ranges['Travel_End_Date'] = pd.to_datetime(df_ranges['Travel_End_Date'])

    # define the timeframe between rows in output csv, 1 day
    delta = timedelta(days=1)

    # open the output CSV file
    with open(output_filename, 'w', newline='') as csv_output_file:
        csv_output_writer = csv.writer(
            csv_output_file, quoting=csv.QUOTE_MINIMAL)

        # write the header lines in output CSV file
        fieldnames = ['date', 'year_week_number', 'is_travel_day']
        csv_output_writer.writerow(fieldnames)

        # iterate through each row in the pandas dataframe
        for ind in df_ranges.index:
            start_date = df_ranges['Travel_Start_Date'][ind]
            end_date = df_ranges['Travel_End_Date'][ind]

            # iterate through each date range, output them to new CSV file
            while start_date <= end_date:
                row_date = start_date.strftime("%Y-%m-%d")
                iter_week_num = str(start_date.weekofyear).zfill(2)
                iter_year = str(start_date.year)
                iter_year_with_week = iter_year + YEAR_WEEK_CONCATENATOR + iter_week_num
                csv_output_writer.writerow(
                    [row_date, iter_year_with_week, True])
                start_date += delta

        # display the output filename
        print(output_filename)


if __name__ == "__main__":
    main(sys.argv[1:])
