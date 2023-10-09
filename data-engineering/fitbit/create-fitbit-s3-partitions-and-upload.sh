#!/bin/bash
# Tim H 2023

# upload fitbit files to S3:
# https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/index.html

LOCAL_PATH_TO_FITBIT_FILES="$HOMER/Downloads/FitBit-export-2023-09-12"

S3_BUCKET_NAME="honk-homelab-datalake-c3ec6660f345c0a719b8"
S3_FIRST_PREFIX="raw_unstructured_original_files/health/fitbit"
S3_URI_PREFIX="s3://${S3_BUCKET_NAME}/${S3_FIRST_PREFIX}"

cd "$LOCAL_PATH_TO_FITBIT_FILES" || exit 1
LIST_OF_FILES_TO_PARSE=$(find . -type f -iname '*20*-*-*.json' )

while IFS= read -r iter_filepath_to_parse
do
    ITER_FILENAME=$(basename "$iter_filepath_to_parse")
    FITBIT_CONTENT_NAME=$(echo "$ITER_FILENAME" | cut -d '-' -f1)
    FITBIT_YEAR=$(echo "$ITER_FILENAME" | cut -d '-' -f2)
    echo "$iter_filepath_to_parse --> $ITER_FILENAME ---> $FITBIT_CONTENT_NAME and YEAR = $FITBIT_YEAR"

    aws s3 cp "$iter_filepath_to_parse" "$S3_URI_PREFIX/$FITBIT_CONTENT_NAME/$FITBIT_YEAR/"

done <<< "$LIST_OF_FILES_TO_PARSE"

# The user-provided path does not exist.
