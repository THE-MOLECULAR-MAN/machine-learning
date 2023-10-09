#!/bin/bash
# Tim H 2023

# Extract Screen Time history from OSX / IOS

# http://www.mac4n6.com/blog/tag/usage
# https://www.r-bloggers.com/2019/10/spelunking-macos-screentime-app-usage-with-r/
# https://www.doubleblak.com/m/blogPosts.php?id=2

set -e
NOW=$(gdate --iso-8601=seconds)
SHORT_HOSTNAME=$(hostname -s)

# SQL_QUERY_FILENAME="dump-apple-screen-usage-per-day-summary.sql"
# SQL_QUERY_FILENAME="app-usage-simple.sql"
# SQL_QUERY_FILENAME="sqltest1.sql"
# SQL_QUERY_FILENAME="list-zstream-names.sql"
# SQL_QUERY_FILENAME="backlit.sql"
SQL_QUERY_FILENAME="list-devices.sql"

OUTPUT_FILE="apple-screentime-summary-sqlite_${SHORT_HOSTNAME}_${NOW}_${SQL_QUERY_FILENAME}.csv"

sqlite3 -csv -header -readonly \
    "$HOME/Library/Application Support/Knowledge/knowledgeC.db" \
    < "$SQL_QUERY_FILENAME" > "$OUTPUT_FILE"

head -n15 "$OUTPUT_FILE"
# md5sum ./*.csv

echo "$OUTPUT_FILE"
