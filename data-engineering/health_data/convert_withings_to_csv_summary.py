#!/usr/local/bin/python3
# Tim H 2023
"""imports various CSV files from Withings health data, consolidates them
into a single CSV file and formats it correctly"""

# python3 convert_withings_to_csv_summary.py -i '/Users/tim/tmp_datalake/Exercise_Records/Withings-TIM_1694612655-2023-09-13'
# less '/Users/tim/tmp_datalake/Exercise_Records/Withings-TIM_1694612655-2023-09-13/withings-summary.csv'

import csv
import sys
import getopt
import pandas as pd
import datetime
from homelab_data_engineering import add_year_week_of_column

def process_sleep_csv_simplest(path_to_sleep_csv):
    """x"""
    # import the CSV into a Pandas dataframe
    df_working = pd.read_csv(path_to_sleep_csv,header=0)
    
    # convert the data types to timestamps
    df_working['from'] = pd.to_datetime(df_working['from'])
    df_working['to']   = pd.to_datetime(df_working['to'])
    
    # create a new column, date, and use the date of the waking day
    df_working['date'] = pd.to_datetime(df_working['to'], utc=True).dt.date
    
    # create new column, calculate the number of hours in difference
    df_working['time_in_bed_in_hours'] = (df_working['to'] - df_working['from']) / pd.Timedelta('1 hour')
    
    # drop the unused columns
    df_working = df_working.drop(
        ["rem (s)","awake (s)","wake up","Duration to sleep (s)",
         "Duration to wake up (s)","Snoring (s)","Snoring episodes",
         "Average heart rate","Heart rate (min)","Heart rate (max)",
         "Night events"], axis=1)
    
    # re-order the columns
    df_working = df_working[['date', 'from', 'to', 'time_in_bed_in_hours']]
    
    # debug stuff
    print("End of process_sleep_csv_simplest stuff...")
    print(df_working)
    print(df_working.dtypes)
    print(type(df_working['time_in_bed_in_hours'][1]))
    
    # return the new dataframe
    return df_working
    

def main(argv):
    """main"""
    # disable warnings:
    # https://www.dataquest.io/blog/settingwithcopywarning/
    pd.set_option('mode.chained_assignment', None)

    # load in args from command line
    opts, args = getopt.getopt(argv, "hi:o:", ["xlsx_path="])
    for opt, arg in opts:
        if opt == '-h':
            print('convert_withings_to_csv_summary.py -i <path_to_withings_files>')
            sys.exit()
        elif opt in ("-i", "--input"):
            path_to_withings_files = arg
            output_csv_filename = path_to_withings_files + \
                '/withings-summary.csv'

    # import and clean up steps:
    steps_new_column_names = ['date', 'exercise_withings_total_steps_per_day']
    df_steps = pd.read_csv(path_to_withings_files +
                           '/aggregates_steps.csv', header=0,
                           names=steps_new_column_names)
    df_steps['date'] = pd.to_datetime(df_steps['date'], utc=True).dt.date

    # import and clean up distances:
    distance_new_column_names = [
        'date', 'exercise_withings_distance_per_day_in_meters']
    df_distance = pd.read_csv(
        path_to_withings_files + '/aggregates_distance.csv', header=0,
        names=distance_new_column_names)
    df_distance['date'] = pd.to_datetime(df_distance['date'], utc=True).dt.date

    # import and clean up calories earned:
    calories_earned_new_column_names = [
        'date', 'exercise_withings_calories_earned']
    df_calories_earned = pd.read_csv(
        path_to_withings_files + '/aggregates_calories_earned.csv', header=0,
        names=calories_earned_new_column_names)
    df_calories_earned['date'] = pd.to_datetime(df_calories_earned['date'], utc=True).dt.date


    # import and clean up calories passive
    calories_passive_new_column_names = [
        'date', 'exercise_withings_calories_passive']
    df_calories_passive = pd.read_csv(
        path_to_withings_files + '/aggregates_calories_passive.csv', header=0,
        names=calories_passive_new_column_names)
    df_calories_passive['date'] = pd.to_datetime(df_calories_passive['date'], utc=True).dt.date

    df_sleep = process_sleep_csv_simplest(path_to_withings_files + '/sleep.csv')
    

    # merge all four into a single data frame, joining on the date
    merged_df = df_steps.merge(df_distance,          on='date', how='outer')
    merged_df = merged_df.merge(df_calories_earned,  on='date', how='outer')
    merged_df = merged_df.merge(df_calories_passive, on='date', how='outer')
    

    # create a new column that is the sum of the two calorie types
    merged_df['exercise_withings_total_calories'] = \
        merged_df['exercise_withings_calories_passive'] + \
        merged_df['exercise_withings_calories_earned']

    # formatting columns as integers, getting rid of decimal places
    merged_df['exercise_withings_total_calories'] = \
        merged_df['exercise_withings_total_calories'].astype(int)

    merged_df['exercise_withings_total_steps_per_day'] = \
        merged_df['exercise_withings_total_steps_per_day'].astype(int)

    merged_df['exercise_withings_distance_per_day_in_meters'] = \
        merged_df['exercise_withings_distance_per_day_in_meters'].astype(int)

    # convert date column to timestamp format, required for add_year_week
    # merged_df['date'] = pd.to_datetime(merged_df['date'])
    
    print('source dataformat: ' + str(type(merged_df['date'][1])) + ' sleep date format: ' + str(type(df_sleep['date'][1])))
    merged_df = merged_df.merge(df_sleep,            on='date', how='outer')

    # sort rows by date ascending
    merged_df = merged_df.sort_values(by='date')

    # remove unused columns
    merged_df = merged_df.drop(['exercise_withings_calories_passive',
                                'exercise_withings_calories_earned'], axis=1)

    # add_year_week_of_column(merged_df)

    # re-order the columns for output
    # merged_df = merged_df[['date',
    #                        'exercise_withings_total_steps_per_day',
    #                        'exercise_withings_distance_per_day_in_meters',
    #                        'exercise_withings_total_calories']]

    print(merged_df)
    print(merged_df.dtypes)

    # output result to CSV file
    merged_df.to_csv(output_csv_filename, header=True, index=False,
                     quoting=csv.QUOTE_NONNUMERIC)

    print(output_csv_filename)


if __name__ == "__main__":
    main(sys.argv[1:])
