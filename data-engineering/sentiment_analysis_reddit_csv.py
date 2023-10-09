#!/usr/local/bin/python3
# Tim H 2023
"""UNFINISHED"""

# python3 sentiment-analysis-reddit-csv.py -i '/Users/tim/Downloads/Reddit-user-dump-2023_09_30_04_02_AM_-0400/Reddit-user-dump-comments-combined.csv'
# head '/Users/tim/Downloads/Reddit-user-dump-2023_09_30_04_02_AM_-0400/Reddit-user-dump-comments-combined.csv-analysis.csv'

import csv
import sys
import getopt
# from datetime import timedelta
# import json
import pandas as pd
import boto3
import numpy as np
from botocore.exceptions import ClientError


def get_sentiment(statement_to_analyze):
    """x"""
    try:
        client = boto3.client('comprehend')
        response_as_dict = client.detect_sentiment(
            Text=statement_to_analyze, LanguageCode='en')
    except ClientError:
        # logger.exception("Couldn't detect sentiment.")
        print("Couldn't detect sentiment.")
        raise
    return response_as_dict


def get_sentiments(array_of_statements):
    """x"""
    try:
        max_documents = 25
        client = boto3.client('comprehend')
        num_statements = len(array_of_statements)
        index_high = 0

        df_responses = pd.DataFrame(columns=['body', 'sentiment_primary_str', 'sentiment_score_positive', 'sentiment_score_negative', 'sentiment_score_neutral', 'sentiment_score_mixed'],
                                    dtype={'body': 'str', 'sentiment_primary_str': 'str', 'sentiment_score_positive': 'float', 'sentiment_score_negative': 'float', 'sentiment_score_neutral': 'float', 'sentiment_score_mixed': 'float'})

        df_responses = array_of_statements
        print(df_responses)

        if num_statements <= 0:
            print("no statements to evaluate")
            sys.exit(2)
            # raise
        if isinstance(array_of_statements, str):
            print("it was a plain string, not an array")
            # whatever

        elif num_statements == 1:
            print("only 1 statement to evalute")
            # whatever[0]

        elif 2 <= num_statements <= max_documents:
            print("2 to 25 statements to evaluate")
            index_high = num_statements - 1
            # whatever []
        elif num_statements > 25:
            print("More than 25 statements to evaluate, need to iterate")
            ind = 0
            while ind < num_statements - 1:
                # the next index will be the lowest number between: the end of
                # the array OR the current iterator plus 25
                index_high = min(num_statements - 1, ind + max_documents - 1)
                print(index_high)
                # whatever [ind:ind_high]
                ind = index_high

            return 0
        else:
            print("unknown number of statementts.")
            sys.exit(1)

        response_as_dict = client.batch_detect_sentiment(
            Text=array_of_statements[0:index_high], LanguageCode='en')

    except ClientError:
        print("Couldn't detect sentiment.")
        raise
    return response_as_dict


def main(argv):
    """main"""
    # load arguments from command line
    input_filename = ''
    output_filename = ''
    opts, args = getopt.getopt(argv, "hi:o:", ["i="])
    for opt, arg in opts:
        if opt == '-h':
            print('sentiment-analysis-reddit-csv.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input_filename = arg
            output_filename = input_filename + "-analysis.csv"

    # load the CSV into a pandas dataframe

    # .created_utc,.subreddit_name_prefixed,.link_title,.link_url,
    # .link_author,.author,.body,.edited

    comment_history_column_names = ['created_utc', 'subreddit_name_prefixed',
                                    'link_title', 'link_url', 'link_author',
                                    'author', 'body', 'edited']

    df_comments = pd.read_csv(input_filename, header=None,
                              names=comment_history_column_names)

    # drop everyting but the timestamp, title, and body
    df_comments = df_comments.loc[:,
                                  df_comments.columns.intersection(['created_utc', 'body'])]

    df_comments['sentiment_primary_str'] = 'uninitialized'

    df_comments['sentiment_score_positive'] = np.nan
    df_comments['sentiment_score_negative'] = np.nan
    df_comments['sentiment_score_neutral'] = np.nan
    df_comments['sentiment_score_mixed'] = np.nan

    # sentiments_array = df_comments['body']

    for ind in df_comments.index:
        comment_to_analyze = df_comments['body'][ind]
        sentiment_response_as_dict = get_sentiment(comment_to_analyze)
        print(sentiment_response_as_dict)

        df_comments['sentiment_primary_str'][ind] = sentiment_response_as_dict['Sentiment']
        df_comments['sentiment_score_positive'][ind] = sentiment_response_as_dict['SentimentScore']['Positive']
        df_comments['sentiment_score_negative'][ind] = sentiment_response_as_dict['SentimentScore']['Negative']
        df_comments['sentiment_score_neutral'][ind] = sentiment_response_as_dict['SentimentScore']['Neutral']
        df_comments['sentiment_score_mixed'][ind] = sentiment_response_as_dict['SentimentScore']['Mixed']

        # print(df_comments)

        # exit(0)

    df_comments.to_csv(output_filename, header=True, index=False,
                       quoting=csv.QUOTE_NONNUMERIC)

    print(output_filename)


if __name__ == "__main__":
    main(sys.argv[1:])
