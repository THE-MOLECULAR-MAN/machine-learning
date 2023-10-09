#!/bin/bash
# Tim H 2023

# backup OS X screentime data to S3
set -e

S3_BUCKET_PREFIX='s3://honk-homelab-datalake-c3ec6660f345c0a719b8/raw_unstructured_original_files/osx-screentime'

DBFILE="$HOME/Library/Application Support/Knowledge/knowledgeC.db"
myhostname=$(hostname -s)
CURRENT_YEAR=$(gdate +"%Y")
CURRENT_MONTH=$(gdate +'%m')
CURRENT_DAY=$(gdate +'%d')

S3_PARTITION_PATH="$CURRENT_YEAR/$CURRENT_MONTH/$CURRENT_DAY"

#echo "Copying knowledgeC.db to S3..."
aws s3 cp "$DBFILE"      "$S3_BUCKET_PREFIX/$S3_PARTITION_PATH/knowledgeC.db"

echo "Dumping SQLite DB to local CSV..."
CSV_FILES=$(./dump-apple-sqlite-to-csv.sh)

echo "Copying local CSV files to S3..."
aws s3 cp $(pwd) "$S3_BUCKET_PREFIX/$S3_PARTITION_PATH/" --recursive --exclude "*" --include "${CSV_FILES}*"

# Delete local CSV files that were just created
rm -f "${CSV_FILES}*"

echo "Dumping SQLite DB to local .SQL file..."
SQL_FILE=$(./dump-apple-sqlite-to-sql.sh)

echo "Copying local .SQL file to S3..."
aws s3 cp "./$SQL_FILE" "$S3_BUCKET_PREFIX/$S3_PARTITION_PATH/"

rm -f "./$SQL_FILE"

echo "contents of S3 location:
"

aws s3 ls "$S3_BUCKET_PREFIX/$S3_PARTITION_PATH/"

echo "

backup-osx-screentime-tos3.sh successfully finished."
