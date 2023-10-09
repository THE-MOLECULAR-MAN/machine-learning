#!/bin/bash
# Tim H 2023

# Finding semi-structured files on Synology

find /volume1 -type f \( -iname "*.csv" -o -iname "*.xml" -o -iname "*.json" \
    -o -iname "*.xml" -o -iname "*.eml" \) \
    ! -name 'package.json' ! -path '*@*' ! -ipath '*plex*' \
    ! -ipath '*node*' ! -ipath '*httrack*' ! -ipath '*web_archiving*' \
    2>/dev/null
