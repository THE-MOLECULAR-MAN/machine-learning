#!/bin/bash
# Tim H 2023

# Transforming Fitbit weight files into CSV
# results are not necessarily sorted

# path to top level directory that has fitbit export
SOURCE_DIR="$HOME/tmp_datalake/Exercise_Records/FitBit-export-2023-09-12/username/Personal & Account"
SINGULAR_OUTPUT_FILE="$SOURCE_DIR/output.csv"

rm "$SINGULAR_OUTPUT_FILE"
cd "$SOURCE_DIR" || exit 1
jq -r '.[] | [.date, .weight] | @csv' "$SOURCE_DIR"/weight-*.json > TMP && mv TMP "$SINGULAR_OUTPUT_FILE"
cat "$SINGULAR_OUTPUT_FILE"
