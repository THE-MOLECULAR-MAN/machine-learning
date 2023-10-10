#!/bin/bash
# Tim H 2023

# Finding semi-structured files on Synology

find /volume1 -type f \( -iname "*.csv" -o -iname "*.xml" -o -iname "*.json" \
    -o -iname "*.eml"  -o -iname '*.har'  -o -iname '*.chlsj' \) \
    ! -name 'package.json' ! -path '*@*' ! -ipath '*plex*' \
    ! -ipath '*node*' ! -ipath '*httrack*' ! -ipath '*web_archiving*' \
    ! -path '*homelab-public*' \
    2>/dev/null

# -o -iname '*.xlsx'  -o -iname '*.xls' -o -iname '*.zip' 
