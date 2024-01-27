#!/usr/local/bin/python3
# Tim H 2023
"""This is a library of reused functions for my data engineering."""
# This script is not directly executable.

import sys
import csv
import getopt
import pathlib
import re

import pandas as pd

# __name__ = 'homelab_data_engineering'

YEAR_WEEK_CONCATENATOR = '_wk_'

REPLACE_LIST_IN_CHAR = {"himself": "",
                        "herself": "",
                        "themself": "",
                        " and ": ";",
                        ",": ";",
                        "  ": " ",
                        ";;": ";"}


def replace_all(text, dic):
    """searches a string and replaces all instances of found key/values """
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def replace_all_as_str(text: str, dic: dict) -> str:
    """searches a string and replaces all instances of found key/values """
    for i, j in dic.items():
        text = text.replace(i, j)
    return str(text)


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
            output_filename = pathlib.Path(
                input_filename).with_suffix(new_suffix)
            return input_filename, output_filename


def load_json_file_into_pandas_dataframe(input_filename):
    """Load a .JSON file into a Pandas Dataframe"""
    return pd.read_json(input_filename)


def load_csv_file_into_pandas_dataframe(input_filename):
    """Load a .CSV file into a Pandas Dataframe"""
    return pd.read_csv(input_filename)


def output_dataframe_to_csv(df_working, output_filename):
    """Write out a Pandas dataframe to a CSV file, including headers
    and quote all non-numeric characters
    designed for training data"""
    df_working.to_csv(output_filename, header=True, index=False,
                      quoting=csv.QUOTE_NONNUMERIC)


def output_dataframe_to_csv_without_header(df_working, output_filename):
    """Write out a Pandas dataframe to a CSV file, WITHOUT headers
    and quote all non-numeric characters
    Designed for test data"""
    df_working.to_csv(output_filename, header=False, index=False,
                      quoting=csv.QUOTE_NONNUMERIC)


def convert_cbb_guest_instance_to_dict(single_guest_appearance_as_str):
    """Converts a string that has a single guest and one or more characters
    a list of actors (Guests) and a list of characters they play"""
    # make sure it's not empty string
    assert len(single_guest_appearance_as_str) > 0

    # make sure it doesn't have a reserved delimiter in it
    assert not re.search(';', single_guest_appearance_as_str)

    # if the guest plays at least one character, it will have ' as ' in it
    if re.search(' as ', single_guest_appearance_as_str):
        # extract guest name and list of characters
        actor_name,  character_list_as_str = single_guest_appearance_as_str.split(
            ' as ', 1)
        # strip out "as himself" or "as herself" and other non-characters
        character_list_as_array = replace_all(
            character_list_as_str, REPLACE_LIST_IN_CHAR).split(';')
        if '' in character_list_as_array:
            character_list_as_array.remove('')
        # remove both leading and trailing whitespace from the character name
        character_list_as_array = [i.strip() for i in character_list_as_array]
        return actor_name, character_list_as_array
    else:
        # guest doesn't play a character, just themselves
        # return an empty array for character list
        # assert not re.search(',', single_guest_appearance_as_str)
        # assert not re.search('/', single_guest_appearance_as_str)
        return single_guest_appearance_as_str, []


def convert_cbb_guest_and_character_list(single_episode_guest_list_str):
    """Takes the ; delimited list of guests and characters for a single
    episode. Converts them into two arrays: one for guests (actors) and one
    for characters"""

    # split out the episode guest list string into an array using the delimiter
    single_episode_guest_list_array = single_episode_guest_list_str.split(';')

    # define empty arrays
    actors = []
    characters = []

    # iterate through each guest/actor and what characters they play (if any)
    for iter_str in single_episode_guest_list_array:
        next_actor, next_character = convert_cbb_guest_instance_to_dict(
            iter_str)

        # add the actor if there is one
        if len(next_actor) > 0:
            actors.append(next_actor)

        # add the character(s) if there are at least 1
        if len(next_character) > 0:
            characters = characters + next_character

    return actors, characters


def convert_cbb_guest_and_character_list2(single_episode_guest_list_str: str) -> list['str']:
    """Takes the ; delimited list of guests and characters for a single
    episode. Converts them into two arrays: one for guests (actors) and one
    for characters"""

    # split out the episode guest list string into an array using the delimiter
    single_episode_guest_list_array = single_episode_guest_list_str.split(';')

    # define empty arrays
    actors = ""
    characters = "none"

    # iterate through each guest/actor and what characters they play (if any)
    for iter_str in single_episode_guest_list_array:
        next_actor, next_character = convert_cbb_guest_instance_to_strings(
            iter_str)
        
        print('next actors ' + str(type(next_actor)) + ' ' + str(next_actor))
        print('next chars  ' + str(type(next_character)) + ' ' + str(next_character))

        # add the actor if there is one
        if len(next_actor) == 0:
            continue
        # elif type(next_actor)
        else:
            #print(type(next_actor))
            #print(next_actor)
            if actors == "":
                actors = str(next_actor)
            else:
                next_actor = str(next_actor)
                actors = str(actors) + ';' + str(next_actor)

        # add the character(s) if there are at least 1
        if len(next_character)  == 0:
            continue
        elif len(next_character) == 1:
            characters = next_character[0]
        else:
            # print(type(next_character))
            #print(next_character)
            
            for ch in next_character:
                if characters == "none":
                    characters = str(ch)
                else:
                    characters = str(characters) + ';' + str(ch)

    return str(actors), str(characters)





def convert_cbb_guest_instance_to_strings(single_guest_appearance_as_str: str) -> list('str'):
    """Converts a string that has a single guest and one or more characters
    a list of actors (Guests) and a list of characters they play"""
    # make sure it's not empty string
    assert len(single_guest_appearance_as_str) > 0

    # make sure it doesn't have a reserved delimiter in it
    assert not re.search(';', single_guest_appearance_as_str)

    # if the guest plays at least one character, it will have ' as ' in it
    if re.search(' as ', single_guest_appearance_as_str):
        # extract guest name and list of characters
        actor_name,  character_list_as_str = single_guest_appearance_as_str.split(
            ' as ', 1)
        # strip out "as himself" or "as herself" and other non-characters
        character_list_as_array = replace_all_as_str(
            character_list_as_str, REPLACE_LIST_IN_CHAR).split(';')
        if '' in character_list_as_array:
            character_list_as_array.remove('')
        # remove both leading and trailing whitespace from the character name
        character_list_as_array = [i.strip() for i in character_list_as_array]
        return str(actor_name), character_list_as_array
    else:
        # guest doesn't play a character, just themselves
        # return an empty array for character list
        # assert not re.search(',', single_guest_appearance_as_str)
        # assert not re.search('/', single_guest_appearance_as_str)
        return str(single_guest_appearance_as_str), ""
