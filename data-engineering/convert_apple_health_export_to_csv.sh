#!/bin/bash
# Tim H 2023

# Converting Apple Health export into usable format

PATH_TO_APPLE_EXPORT="/Volumes/tim_carrie_shared/data_sets/health/apple_health_export-2023-10-09"
PATH_TO_CONVERTER_SCRIPT="$HOME/source_code/third_party/Simple-Apple-Health-XML-to-CSV/apple_health_xml_convert.py"
FIRST_CSV_FILENAME="apple_health_export_2023-10-09.csv"
SORTED_CSV_FILENAME="apple_health_export_2023-10-09-sorted.csv"

if [[ ! -f "$PATH_TO_APPLE_EXPORT/export.xml" ]]; then
    echo "output.xml file doesn't exist. Exiting."
    ls -lah "$PATH_TO_APPLE_EXPORT"
    exit 1
fi

# copy the XML to CSV script over to data repo
cp -n "$PATH_TO_CONVERTER_SCRIPT" "$PATH_TO_APPLE_EXPORT/"

cd "$PATH_TO_APPLE_EXPORT" || exit 1

# run the script, it'll create a new CSV file
if [[ ! -f "$FIRST_CSV_FILENAME" ]]; then
    echo "Converting XML to CSV..."
    python3 apple_health_xml_convert.py
else
    echo "CSV file already existed, skipping."
fi

if [[ ! -f "$SORTED_CSV_FILENAME" ]]; then
    echo "Sorting CSV file..."
    (head -n 1 "$FIRST_CSV_FILENAME" && tail -n +2 "$FIRST_CSV_FILENAME" | sort --field-separator ',' -k 1,1 -k 2,2 -k 5,5) > "$SORTED_CSV_FILENAME"
else
    echo "Sorted CSV already exists, skipping."
fi

head "$SORTED_CSV_FILENAME"

# show all instances of the header in the output file. Should only be 1.
# grep -n sourceName apple_health_export_2023-10-09-sorted.csv

echo "Script finished successfully."
