#!/bin/bash
# Tim H 2023

# Apple knowledgedb backup - sqlite3
# similar to pg_dumpall in Postgresql
set -e

DBFILE="$HOME/Library/Application Support/Knowledge/knowledgeC.db"
NOW=$(gdate --iso-8601=seconds)
myhostname=$(hostname -s)
output_filename="apple-screentime-sql-full-backup_${myhostname}_${NOW}.sql"

echo "-- backup generated: $NOW
-- on system: $myhostname" > "$output_filename"

echo ".dump" | sqlite3 -readonly "$DBFILE" >> "$output_filename"

echo "$output_filename"
