#!/bin/bash
# Tim H 2023

# Convert XML to JSON
# https://validator.w3.org/feed/check.cgi
# https://www.howtogeek.com/devops/how-to-convert-xml-to-json-on-the-command-line/
# https://www.geeksforgeeks.org/python-xml-to-json/
# https://www.baeldung.com/linux/xmllint
# https://jsonlint.com/
# https://stackoverflow.com/questions/36317381/how-to-use-xmllint-to-validate-an-xml-document-with-an-xsd

set -e

XML_FILE_TO_CONVERT="./podcasts/comedybangbang.xml"
OUTPUT_FILE="./podcasts/comedybangbang.json"
OUTPUT_FILE_SIMPLIFIED="./podcasts/comedybangbang_simplified.json"

# mark file as read-only just in case I make changes
chmod -wx "$XML_FILE_TO_CONVERT"

# XML_SCHEMA_URL="http://www.itunes.com/dtds/podcast-1.0.dtd"
# XML_SCHEMA_URL="http://www.google.com/schemas/play-podcasts/1.0"
# XML_SCHEMA_URL="https://www.google.com/schemas/play-podcasts/1.0/play-podcasts.xsd"
# xmllint --noout --valid --nonet --huge "$XML_FILE_TO_CONVERT"
# --valid --schema "$XML_SCHEMA_URL"

# check the XML file for issues before assuming it is valid
xmllint --noout  --quiet  "$XML_FILE_TO_CONVERT" || echo "XML Lint failed"

# convert the XML file to JSON
xq . "$XML_FILE_TO_CONVERT" > "$OUTPUT_FILE"

# check the initial JSON file for issues
jsonlint --quiet "$OUTPUT_FILE" || echo "JSON Lint failed"

# extract just the podcast episodes into a new JSON file
jq '.rss.channel.item' "$OUTPUT_FILE" > "$OUTPUT_FILE_SIMPLIFIED"

# check the new JSON file for syntax issues
jsonlint --quiet "$OUTPUT_FILE_SIMPLIFIED" || echo "JSON Lint failed"

echo "convert-xml-to-json.sh finished successfully."
