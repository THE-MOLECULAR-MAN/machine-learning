#!/bin/bash
# Tim H 2023

set -e

# Apple knowledgedb backup - sqlite3
DBFILE="$HOME/Library/Application Support/Knowledge/knowledgeC.db"
myhostname=$(hostname -s)
NOW=$(gdate --iso-8601=seconds)

# obtain all data tables from database
tables=$(sqlite3 "$DBFILE" "SELECT tbl_name FROM sqlite_master WHERE type='table' and tbl_name not like 'sqlite_%';")

# iterate through list of tables, dump each one to a separate CSV file
while IFS= read -r table_name || [[ -n $table_name ]]; do
    output_filename="apple-screentime-csv-tables_${myhostname}_${NOW}_${table_name}.csv"

    # dump it to CSV    
    sqlite3 -csv -header "$DBFILE" "select * from $table_name;" > "$output_filename"

    # display the filename
    # echo "$output_filename"

done < <(printf '%s' "$tables")

echo "apple-screentime-csv-tables_${myhostname}_${NOW}_"
