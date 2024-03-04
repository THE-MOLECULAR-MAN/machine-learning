#!/usr/local/bin/python3
# Tim H 2023
"""Python script for converting a single column in a CSV file from a comma
delimited string into a new column that uses an array for each item in the 
comma delimited string.

For Example - original file:
col1,col2
"Andy Daly, Paul F. Tompkins",400

becomes new CSV file
col1,col2,col3
"Andy Daly, Paul F. Tompkins",400,['Andy Daly', 'Paul F Tompkins']

"""

# example Bash call:
# python3 ./convert_comma_delimited_string_column_to_array.py -i "$HOME/Downloads/Comedy_bang_bang_podcast_dataset - full_dataset.csv"
# head '/Users/redacted/Downloads/Comedy_bang_bang_podcast_dataset-v2.csv-array-converted.csv'

import csv
import sys
import getopt
import pandas as pd


def main(argv):
    """main"""
    # disable warnings:
    # https://www.dataquest.io/blog/settingwithcopywarning/
    pd.set_option('mode.chained_assignment', None)

    # load in args from command line
    # pylint: disable=unused-variable
    opts, args = getopt.getopt(argv, "hi:o:", ["xlsx_path="])
    for opt, arg in opts:
        if opt == '-h':
            print('convert-comma-delimited-string-column-to-array.py -i <path_to_csv>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input_filename = arg
            output_filename = input_filename + '-array-converted.csv'

    df_data = pd.read_csv(input_filename, header=0)

    column_name_to_convert = 'guests_and_characters_from_wikipedia_semicolon_delimited'
    new_column_name = 'guest_list_as_array'

    # next line has the issue
    df_data[new_column_name] = df_data[column_name_to_convert].str.split(',')

    print(df_data)
    print(df_data.dtypes)

    # output result to CSV file
    df_data.to_csv(output_filename, header=True, index=False,
                   quoting=csv.QUOTE_NONNUMERIC)

    print(output_filename)


if __name__ == "__main__":
    main(sys.argv[1:])
