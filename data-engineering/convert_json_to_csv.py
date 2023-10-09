#!/usr/local/bin/python3
# Tim H 2023
"""x"""

# rm -f '/Users/tim/Downloads/PitPat_reverse_engineering/pitpat_daily_dump_2023-04-05_to_2023-10-02.csv' && python3 convert_json_to_csv.py -i '/Users/tim/Downloads/PitPat_reverse_engineering/pitpat_daily_dump_2023-04-05_to_2023-10-02.json'
# head '/Users/tim/Downloads/PitPat_reverse_engineering/pitpat_daily_dump_2023-04-05_to_2023-10-02.csv'

import sys
import csv
import getopt
import pathlib

import pandas as pd

import homelab_data_engineering as hme


def main(argv):
    """main"""

    input_filename,output_filename = hme.get_input_output_files(argv, '.csv')

    # read a JSON file directly into a Pandas Dataframe
    df_working = hme.load_json_file_into_pandas_dataframe(input_filename)

    # output a Pandas Dataframe into a CSV file including the headers
    hme.output_dataframe_to_csv(df_working, output_filename)

    print(output_filename)


if __name__ == "__main__":
    main(sys.argv[1:])
