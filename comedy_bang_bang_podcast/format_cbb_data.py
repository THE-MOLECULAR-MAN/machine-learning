#!/usr/local/bin/python3
# Tim H 2023
"""Creates training data and test data sets formatted for SageMaker
Output the Google Sheet as CSV and give it to this script
This script produces two CSV files"""

# import numpy as np
import homelab_data_engineering as hde

output_file_prefix='/Volumes/tim_carrie_shared/S3_sync_datalake----2/data-sets/comedy_bang_bang_podcast/Comedy_bang_bang_podcast_dataset - full_dataset-v15'

df = hde.load_csv_file_into_pandas_dataframe(output_file_prefix + '.csv')

df['actors'] = [[]] * len(df.index)
df['characters'] = [[]] * len(df.index)

colunn_output_order = ['data_set', 'episode_number', 'date_episode_published',
                       'year_elligible_for_best_of', 'duration_in_minutes', 
                       'episode_type',                     
                       'actors', 'characters',
                       'weight_flat', 'weight_inverse', 'weight_linear',
                       'is_on_best_of_boolean']

# 'episode_title','synopsis_and_segments',

for ind in df.index:
    orig = df['guests_and_characters_from_wikipedia_semicolon_delimited'][ind]
    actors, characters = hde.convert_cbb_guest_and_character_list2(orig)
    df['actors'][ind] = actors
    df['characters'][ind] = characters

df = df[colunn_output_order]

# drop unused columns:
# df.drop(['episode_title', 'synopsis_and_segments',
# 'guests_and_characters_from_wikipedia_semicolon_delimited',
# 'fandom_wikia_suffix', ], axis=1, inplace=True)

# format episode_number as integer, drop the decimal
df = df.astype({'episode_number':'int'})
# arr = df['actors'].to_numpy()
#df['actors'] = '[0, 1, 2, 3]'

import numpy as np

# target = np.array(['dog', 'dog', 'cat', 'cat', 'cat', 'dog', 'dog', 
#     'cat', 'cat', 'hamster', 'hamster'])

def one_hot(array):
    unique, inverse = np.unique(array, return_inverse=True)
    onehot = np.eye(unique.shape[0])[inverse]
    return onehot

print(one_hot(target))

#print(df['characters'])
#print(df.dtypes)
# print(df.ctypes)

df_training   = df.query('data_set == "training"').sort_values(by=['episode_number'])
df_prediction = df.query('data_set == "prediction"').sort_values(by=['episode_number'])

# drop the data_set column on the training data
df_training = df_training.drop(columns=['data_set'])

# drop the data_set and TARGET column on the test data
df_prediction = df_prediction.drop(
    columns=['is_on_best_of_boolean', 'data_set'])

hde.output_dataframe_to_csv(df_training,                  output_file_prefix + '-training.csv')
hde.output_dataframe_to_csv_without_header(df_prediction, output_file_prefix + '-prediction.csv')
