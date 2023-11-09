#!/usr/local/bin/python3
# Tim H 2023
"""Creates training data and test data sets formatted for SageMaker
Output the Google Sheet as CSV and give it to this script
This script produces two CSV files"""


# import numpy as np
import homelab_data_engineering as hde

df = hde.load_csv_file_into_pandas_dataframe(
    '/Users/tim/Downloads/Comedy_bang_bang_podcast_dataset-full_dataset-v10.csv')

df['actors'] = [[]] * len(df.index)
df['characters'] = [[]] * len(df.index)

colunn_output_order = ['data_set', 'episode_number', 'date_episode_published',
                       'year_elligible_for_best_of', 'duration_in_minutes', 'episode_type',
                       'episode_was_split', 'episode_title',
                       'synopsis_and_segments', 'actors', 'characters',
                       'weight', 'is_on_best_of_boolean']

for ind in df.index:
    orig = df['guests_and_characters_from_wikipedia_semicolon_delimited'][ind]
    actors, characters = hde.convert_cbb_guest_and_character_list(orig)
    df['actors'][ind] = actors
    df['characters'][ind] = characters

df = df[colunn_output_order]

df_training = df.query('data_set == "training"')
df_prediction = df.query('data_set == "prediction"')

df_training = df_training.drop(columns=['data_set'])
df_prediction = df_prediction.drop(
    columns=['is_on_best_of_boolean', 'data_set'])

hde.output_dataframe_to_csv(df_training,                  'cbb-training.csv')
hde.output_dataframe_to_csv_without_header(df_prediction, 'cbb-prediction.csv')
