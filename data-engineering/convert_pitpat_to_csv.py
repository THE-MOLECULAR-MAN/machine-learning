#!/usr/local/bin/python3
# Tim H 2023
"""x"""

# rm -f '/Users/tim/Downloads/PitPat_reverse_engineering/pitpat_daily_dump_2023-04-05_to_2023-10-02.csv' && python3 convert_pitpat_to_csv.py -i '/Users/tim/Downloads/PitPat_reverse_engineering/pitpat_daily_dump_2023-04-05_to_2023-10-02.json' && head '/Users/tim/Downloads/PitPat_reverse_engineering/pitpat_daily_dump_2023-04-05_to_2023-10-02.csv'
# 

import sys
import csv
import getopt
import pathlib

import pandas as pd

import homelab_data_engineering as hme

# {
#     "Blocks": 144,
#     "DogId": "79d85a8e-741c-4f29-a7c2-c1b79213c6ee",
#     "Date": "2023-09-30T00:00:00Z",
#     "TotalWalkMinutes": 50,
#     "TotalRunMinutes": 10,
#     "TotalPlayMinutes": 15,
#     "TotalPotteringMinutes": 295,
#     "TotalRestMinutes": 1070,
#     "AggregatedEffort": 24.03,
#     "TotalCalories": 560,
#     "WeightKg": 13.15417873,
#     "UserGoal": 30,
#     "RecommendedGoal": 30,
#     "Activeness": 75,
#     "RecommendedGoalAchieved": true,
#     "UserGoalAchieved": true,
#     "TotalSteps": 37258,
#     "TotalDistance": 4354.52875,
#     "EarliestDataTime": "2023-09-30T04:00:00Z",
#     "LatestDataTime": "2023-10-01T03:50:00Z",
#     "SumOfBlockEffortSquares": 83148.0,
#     "UpdateTime": "2023-10-02T23:43:18.7455237Z"
#   },


def main(argv):
    """main"""

    input_filename,output_filename = hme.get_input_output_files(argv, '.csv')

    # read a JSON file directly into a Pandas Dataframe
    df_working = hme.load_json_file_into_pandas_dataframe(input_filename)
    
    # drop unused columns
    df_working = df_working.drop(['Blocks', 'DogId', 'WeightKg', 'UserGoal', 
                     'RecommendedGoal', 'RecommendedGoalAchieved', 
                     'UserGoalAchieved', 'UpdateTime', 'EarliestDataTime', 
                     'LatestDataTime' ], axis=1)
    
    # convert the date column to just the date, don't need the time to be midnight
    df_working['Date'] = df_working['Date'].dt.date
    
    # round down the distance, don't need tiny fractions of a foot
    df_working['TotalDistance'] = df_working['TotalDistance'].astype('int64')
    
    # round to remove the dozen extra decimal places.
    df_working['AggregatedEffort'] = df_working['AggregatedEffort'].round(1)
    
    # sort by increasing date - chronological
    df_working = df_working.sort_values(by='Date')
    
    # display datatypes for debugging
    print(df_working.dtypes)
    
    # output a Pandas Dataframe into a CSV file including the headers
    hme.output_dataframe_to_csv(df_working, output_filename)

    print(output_filename)


if __name__ == "__main__":
    main(sys.argv[1:])
